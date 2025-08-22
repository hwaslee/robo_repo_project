import time
import re
from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF


# from RPA.Browser.Selenium import Browser


""" Insert the sales data for the week and export it as a PDF """
@task
def get_product_inventory():
    browser.configure(
        # width=1920,
        # height=1080,
        slowmo=500,
    )
    open_the_getmall_website()
    log_in()
    get_all_product_list()

""" Navigates to the given URL """
def open_the_getmall_website():
    # browser.goto("http://newonpan.getmall.kr/front/login.php?chUrl=%2FB2B%2Fex_order.php")
    browser.goto("http://newonpan.getmall.kr/front/login.php")
    page = browser.page()
    page.set_viewport_size({"width": 1280, "height": 1080})
    
    # browser = Browser()
    # browser.open_available_browser("http://newonpan.getmall.kr/front/login.php?chUrl=%2FB2B%2Fex_order.php")
    
""" Fills in the login form and clicks the 'Log in' button """
def log_in():
    page = browser.page()
    # page.set_viewport_size({"width": 1280, "height": 1080})

    try:
        page.fill('input[name="id"]', "broad9898")
        page.fill('input[name="passwd"]', "good1289")
        
        # page.click('a:has-text("로그인")')                # CSS + text 이용, not working
        # page.click('//a[text()="로그인"]')                # XPATH 이용, not working
        page.click('a[href="JavaScript:CheckForm()"]')    # CSS Selector 이용
        # page().click('button[type="submit"]')           # 버튼이 이님, not working
        
        print("GOTO NEXT PAGE....")
        # Wait for the new URL to load
        page.wait_for_url(url="http://newonpan.getmall.kr/main/main.php", timeout=10000)    # working
                               
        # Now the script can continue interacting with the dashboard page
        print("LOGIN SUCCESSFUL AND DASHBOARD PAGE LOADED....")        
    except Exception as e:
        print(f"ERROR: {e} OCCURRED....")
        exit

''' get the list of all products, separated by page no '''    
def get_all_product_list():
    page = browser.page()        
    page.fill('input[name="search"]', "0")
    page.click('a[href="javascript:TopSearchCheck()"]')
    
    page.wait_for_url(url="http://newonpan.getmall.kr/front/productsearch.php?search=0", timeout=10000) 
    time.sleep(3)

    last_page = get_last_page_no()        
    if last_page < 0:
        print("마지막 페이지 No. 인식 오류, 종료됨")
        exit
        
    print(f'마지막 페이지: {last_page}')
    
    for page_no in range(2, last_page+1):
        goto_page(page_no)
        get_page_products(page_no)
        
        page_no = page_no + 1

    
''' get the number of pages '''
def get_last_page_no():
    # page = browser.page()        
    
    try:
        scroll_trigger_locator = browser.page().locator("//form[1]/div[6]")
        scroll_trigger_locator.scroll_into_view_if_needed()

        # 1. '마지막 페이지' 텍스트를 가진 <a> 요소를 찾음
        # last_page_locator = browser.page().locator('//a[text()="마지막 페이지"]')
        last_page_locator = browser.page().locator("//form[1]/div[6]/a[11]")
        # last_page_locator.wait_for()
        
        # 2. 요소의 'href' 속성 값을 가져옴
        href_value = last_page_locator.get_attribute("href", timeout=3000)
        
        # 3. 정규 표현식으로 'GoPage(X,Y)'에서 Y 값을 추출
        match = re.search(r'GoPage\(\d+,\s*(\d+)\);', href_value)
        
        if match:
            max_page_number = int(match.group(1))
            print(f"마지막 페이지 번호: {max_page_number}")
            return max_page_number
        else:
            print("마지막 페이지 번호를 찾을 수 없습니다.")
            return -1
    except Exception as e:
        print(f"Exception 발생: {e}")
        return -1
    
''' Display products in specified page '''            
def goto_page(page_no):
    page = browser.page()        
    
    page_idx = (page_no - 1) // 10
    # print(f'PG_IDX:{page_idx}, PAGE_NO: {page_no}')

    href_link = f'a[href="javascript:GoPage({page_idx},{page_no});"]'
    browser.page().locator(f'{href_link}').scroll_into_view_if_needed()
    page.click(f'{href_link}')

    pg_url = f'http://newonpan.getmall.kr/front/productsearch.php?block={page_idx}&gotopage={page_no}&sort=&codeA=&codeB=&codeC=&codeD=&minprice=&maxprice=&s_check=all&search=0&search1=&listnum=20'    
    page.wait_for_url(url=pg_url, timeout=5000)    # working
    
''' Access each product in the page '''    
def get_page_products(page_no):    
    page = browser.page()  
    
    body_locator = browser.page().locator("//table/tbody")
    locators = body_locator.all()
    print(f"1.......... PAGE_NO:{page_no}, COUNT: {locators.count}")
    locators = body_locator.get_by_role('tr').all()
    print(f"2.......... PAGE_NO:{page_no}, COUNT: {locators.index}")
    for li in page.get_by_role('tr').all():
        print(li.all_inner_texts())