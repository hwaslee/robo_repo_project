from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF


""" Select python 3.12.8 as defined in conda.yaml """


# *** Settings ***
# Documentation     Template robot main suite.

# *** Tasks ***


@task
def robot_spare_bin_python():
    """ Insert the sales data for the week and export it as a PDF """
    browser.configure(
        slowmo=100,
    )
    open_the_intranet_website()
    log_in()
    download_excel_files()
    fill_form_with_excel_data()
    export_as_pdf()
    collect_results()
    log_out()
    
def open_the_intranet_website():
    """ Navigates to the given URL """
    browser.goto("https://robotsparebinindustries.com/")

def log_in():
    """ Fills in the login form and clicks the 'Log in' button """
    page = browser.page()
    page.fill("#username", "maria")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")

def download_excel_files():
    ''' Download excel file from the given url '''
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/SalesData.xlsx", overwrite=True)
    
def fill_form_with_excel_data():
    ''' Read data from excel and fill in the sales form '''
    excel = Files()
    excel.open_workbook("SalesData.xlsx")    
    worksheet = excel.read_worksheet_as_table("data", header=True)    
    for row in worksheet:
        fill_and_submit_sales_form(row)    
        
    excel.close_workbook()
    
def fill_and_submit_sales_form(sales_rep):
    ''' fill in the sales data and click the 'Submit' button '''
    page = browser.page()
    
    page.fill("#firstname", sales_rep["First Name"])
    page.fill("#lastname", sales_rep["Last Name"])
    page.select_option("#salestarget", str(sales_rep["Sales Target"]))
    page.fill("#salesresult", str(sales_rep["Sales"]))
    page.click("text=Submit")
    
def collect_results():
    " Take a screenshot of the page"
    page = browser.page()
    page.screenshot(path="output/sales_summary.png") 

def log_out():
    """ Press the log-out button """
    page = browser.page()
    page.click("text=Log out")

def export_as_pdf():
    ''' Export the data to a PDF file '''
    page = browser.page()
    div_id_locator = page.locator("#sales-results")
    print(f'div_id_locator: {div_id_locator}')
    sales_results_html = div_id_locator.inner_html()
    print(f'sales_results_html: {sales_results_html}')
    # sales_results_html = page.locator("#sales-results").inner_html()
    
    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, "output/sales_results.pdf")
    
     