import time
import re
import openpyxl
import traceback
import sys
from datetime import datetime
from urllib.parse import urljoin
from urllib.parse import quote
from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF
# from RPA.Browser.Selenium import Browser

keyword = "0"   # "MINE"    # "루어"    # "스트링"  # "루어"    # "다용도"  # "호신"    # "안전"
workbook = ''
sheet = ''
condition = '상품명'      # ''
exclude_list = ['[MINE]']

""" Insert the sales data for the week and export it as a PDF """
@task
def get_product_inventory():
    browser.configure(
        # width=1920,
        # height=1080,
        slowmo=500,
    )
    try: 
        init_excel_file()
        open_the_getmall_website()
        log_in()
        # get_all_product_list()
        get_product_stock()
    except Exception as e:
        print(f'exceptop {e} 발생')
        traceback.print_exc(file=sys.stdout)    # sys.stdout으로 출력하여 콘솔에 보이게 함
    finally:
        close_workbook()
    
''' initialize excel file '''
def init_excel_file():
    global workbook
    global sheet
    
    # 새 workbook (엑셀 파일) 생성
    workbook = openpyxl.Workbook()

    # 현재 활성화된 워크시트 선택 - 기본 시트명 'Sheet'
    sheet = workbook.active
    sheet.title = "온판 재고"
    
    # 셀에 headline 쓰기 - 직접 셀에 접근하여 값을 할당합니다.
    sheet['A1'] = "제품명"
    sheet['B1'] = "기본 가격"
    sheet['C1'] = "옵션명"
    sheet['D1'] = "옵션 가격"
    sheet['E1'] = "재고"

    
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
        page.wait_for_url(url="http://newonpan.getmall.kr/main/main.php", timeout=5000)    # working"
                               
        # Now the script can continue interacting with the dashboard page
        print("LOGIN SUCCESSFUL AND DASHBOARD PAGE LOADED....")        
    except Exception as e:
        print(f"ERROR: {e} OCCURRED....")
        exit


''' access each page and get stock of product in page '''
def get_product_stock():
    global keyword
    page = browser.page()        
    page.fill('input[name="search"]', keyword)
    page.click('a[href="javascript:TopSearchCheck()"]')
    
    # quote() 함수로 URL 인코딩 수행
    encoded_keyword = quote(keyword)
    search_url = f"http://newonpan.getmall.kr/front/productsearch.php?search={encoded_keyword}"
    print(f'=============== 첫 검색 URL: {search_url}')
    page.wait_for_url(search_url, timeout=5000)    
    
    page_no = 1
    while True:
        # extract each product info by clicking product shown up in the screen.
        extract_table_data(page_no)  
                    
        # Page navigation (going to next page)
        # first, click page_no
        page_no = page_no + 1
        page_idx = (page_no - 1) // 10
        href_link = f'a[href="javascript:GoPage({page_idx},{page_no});"]'
        if browser.page().locator(f'{href_link}').is_visible(timeout=500):
            print(f"=============== 다음 페이지로 이동: 방법 1...to Page {page_no}")
            browser.page().locator(f'{href_link}').scroll_into_view_if_needed()
            page.click(f'{href_link}')
            # http://newonpan.getmall.kr/front/productsearch.php?block=0&gotopage=2&sort=&codeA=&codeB=&codeC=&codeD=&minprice=&maxprice=&s_check=all&search=0&search1=&listnum=20

            pg_url = f'http://newonpan.getmall.kr/front/productsearch.php?block={page_idx}&gotopage={page_no}&sort=&codeA=&codeB=&codeC=&codeD=&minprice=&maxprice=&s_check=all&search={encoded_keyword}&search1=&listnum=20'    
            page.wait_for_url(url=pg_url, timeout=5000)    # working
            continue
        
        # next, click "next" 
        # 'prList' 클래스를 가진 <font> 태그 안에 텍스트 '[next]'를 포함하는 요소를 찾아서 클릭
        if browser.page().locator("font.prList:has-text('[next]')").is_visible(timeout=500):
            print(f"=============== 다음 페이지로 이동: 방법 2...to Page {page_no}")
            browser.page().locator("font.prList:has-text('[next]')").click()
            
            # wait
            continue
    
        # 더 간단하게 텍스트만으로 찾기
        if browser.page().locator("[next]").is_visible(timeout=500):
            print(f"=============== 다음 페이지로 이동: 방법 3...to Page {page_no}")
            browser.page().locator("[next]").click()
            
            # wait
            continue         
        
        # 더 이상 페이지가 없으면 break
        print('=============== 더 이상 페이지 없어 종료')
        break


""" 현재 상품 페이지의 테이블 데이터를 순차적으로 추출 """
def extract_table_data(page_no):
    global exclude_list
    
    page = browser.page()
    
    # 테이블의 모든 행(tr) 요소 검색
    # browser.locator("table tr")는 CSS Selector를 사용.
    tr_rows = page.locator("table tbody tr td table tbody").all()

    # tbody는 상품별, 따라서 상품별 반복.
    for row_index, row_element in enumerate(tr_rows):
        print(f"========== PAGE:{page_no}, Product Index: {row_index+1}/{len(tr_rows)}")
        
        # 현재 행(tr) 내부에 대해 locator.all()을 사용하여 여러 개의 요소를 리스트로 모든 셀(td) 검색
        td_cells = row_element.locator("td").all()
        print(f"PAGE:{page_no},  {len(td_cells)} TDs in td_cells ")
        
        # 상품 검색 화면에 비정상적인 상품 및 layout 존재하여, 이 상품들은 skip
        if row_element.locator("p.prname").is_visible(timeout=500):        
            prod_name = row_element.locator("p.prname").text_content(timeout=500)
            if prod_name in exclude_list:
                print(f"PAGE:{page_no}, Product Index: {row_index}, Name: {prod_name} skipped\n")
                continue
               
        href_url = ""
        for cell_index, cell_element in enumerate(td_cells):
            # td 아래 table이 없으면 skip
            if not cell_element.locator('table').is_visible:
                continue
        
            # 각 셀의 href, 상품명을 추출.
            # cell_text = cell_element.text_content()
            # print(f"  > Cell {cell_index + 1}: {cellcell_text}")
            # all_text = cell_element.all_inner_texts
            # print(f"\t1.--- Cell:{cell_index + 1}, {all_text}")
            
            # 2. WORKING, so commented out not to be changed
            # if cell_element.locator('a[href]').is_visible(timeout=500):
            #     href_link = cell_element.locator('a[href]').get_attribute('href', timeout=500)
            #     print(f"\t2.--- href:{href_link}")
            # else:
            #     print(f'"\t2.--- a[href]" is NOT visible')                
                
            # 3. WORKING, so commented out not to be changed    
            xpath_str = "a[href]"   
            if cell_element.locator(xpath_str).is_visible(timeout=500):
                temp_url = cell_element.locator(xpath_str).get_attribute('href', timeout=500)
                # 상품 페이지에 뜬금없이 "태그..."라는 tag가 있어, 이를 무시
                if "tag.php" in temp_url or "GoMinishop" in temp_url:
                    continue
                href_url = temp_url
                print(f"\t3.--- url:{href_url}")
            # else:
            #     print(f'\t3.--- {xpath_str} is NOT visible') 
            
            # 4. WORKING, so commented out not to be changed 
            # 3번째 p.prname에서 유효한 값 추출        
            # xpath_str = "a p.prname"   
            # if cell_element.locator(xpath_str).is_visible(timeout=500):
            #     name_locator = cell_element.locator(xpath_str)
            #     # .get_attribute('prname', timeout=500)
            #     prname = name_locator.text_content()
            #     print(f"\t4.--- prname:{prname}")
            # else:
            #     print(f'\t4.--- {xpath_str} is NOT visible') 
                
            xpath_str = 'p.prprice'
            if cell_element.locator(xpath_str).is_visible(timeout=500):
                prprice = cell_element.locator(xpath_str).text_content(timeout=500)
                print(f"\t5.--- price:{prprice}")
            # else:
            #     print(f'\t5.--- {xpath_str} is NOT visible')       
            #     continue
        
        if href_url != "":
            get_prod_option_data(page_no, href_url)
            print(f"PAGE:{page_no}, Product Index: {row_index} data extraction completed\n")


''' move to prod page and save inventory to excel file '''
def get_prod_option_data(page_no, href_url):
    print(f'\tFor prod in PG:{page_no}, will save the inventory into Excel')
    page = browser.page()
    # Not working, Protocol error (Page.navigate): 
    # Cannot navigate to invalid URL 
    # Call log: navigating to "../front/productdetail.php?productcode=007002000000000073" 
    # browser.goto(href_url)    

    page.click(f'a[href="{href_url}"]')  
    base_url = "http://newonpan.getmall.kr/front/"
    # urljoin() 함수를 사용하여 두 URL을 결합
    absolute_url = urljoin(base_url, href_url)
    page.wait_for_url(url=absolute_url, timeout=5000) 
    
    # access invenrory and save them to excel file
    save_data_to_excel()
    
    print("will go back to prod page")
    browser.page().go_back(timeout=1000)
    
    
''' save data (prodname, price, options,..) to excel file '''    
def save_data_to_excel():
    global workbook
    global sheet
    
    page = browser.page()
    
    prname = page.locator("div.prdetailname").text_content(timeout=500)
    prprice = page.locator("span#idx_price").inner_text(timeout=500)
    print(f'Name:{prname}, Price:{prprice}')
    
    # option 정보를 추출
    select_locator = page.locator("select[class='basic_select']")
    option_locators = select_locator.locator("option").all()
    option_texts = [opt.inner_text() for opt in option_locators] 
    # option_texts = option_texts.replace("\n","").replace("\t","")   
    print(f"type: {type(option_texts)}, Options: {option_texts}, ")
    
    for option in option_texts:
        option_list = option.split('|')
        if any("(필수)" in item for item in option_list) or any("---" in item for item in option_list):
            continue
        row_data = [prname, prprice] + option_list
        sheet.append(row_data)
        
        prname = ' '
        prprice = ' '    
    
    
def close_workbook():
    global workbook
    global sheet
    
    now = datetime.now()
    # YYYY-MM-DD 형식으로 변환
    formatted_date = now.strftime('%y%m%d')        
    filename = 'onpan_inventory_' + formatted_date + ".xlsx"
    
    workbook.save(filename)
    
    
    
    
    
 ##### =======================================================   
    

''' get the list of all products, separated by page no '''    
def get_all_product_list():
    global keyword
    page = browser.page()        
    page.fill('input[name="search"]', keyword)
    page.click('a[href="javascript:TopSearchCheck()"]')
    
    # quote() 함수로 URL 인코딩 수행
    encoded_keyword = quote(keyword)
    search_url = f"http://newonpan.getmall.kr/front/productsearch.php?search={encoded_keyword}"
    print(f'URL: {search_url}')
    page.wait_for_url(search_url, timeout=5000) 

    last_page = get_last_page_no()        
    if last_page < 0:
        print("마지막 페이지 No. 인식 오류, 종료됨")
        exit
    print(f'마지막 페이지: {last_page}')
    
    # page 1
    # get_page_products2(1)
    
    for page_no in range(2, last_page+1):
        goto_page(page_no, keyword)
        prods = get_page_products2(page_no)
        
        page_no = page_no + 1

 
''' get the number of pages '''
def get_last_page_no():
    # page = browser.page()        
    
    try:
        scroll_trigger_locator = browser.page().locator("//form[1]/div[6]")
        scroll_trigger_locator.scroll_into_view_if_needed()

        # 1. '마지막 페이지' 텍스트를 가진 <a> 요소를 찾음
        # last_page_locator = browser.page().locator('//a[text()="마지막 페이지"]')
        last_page_locator = browser.page().locator("//form[1]/div[6]/a[11]")    # "0":working, "안전":not working"
        # last_page_locator = browser.page().locator("//form[1]/div[6]/a")        # "0", "안전":not working"
        # last_page_locator.wait_for()
        
        # 2. 요소의 'href' 속성 값을 가져옴
        href_value = last_page_locator.get_attribute("href", timeout=1000)
        
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
def goto_page(page_no, keyword):
    page = browser.page()        
    
    page_idx = (page_no - 1) // 10
    # print(f'PG_IDX:{page_idx}, PAGE_NO: {page_no}')

    href_link = f'a[href="javascript:GoPage({page_idx},{page_no});"]'
    browser.page().locator(f'{href_link}').scroll_into_view_if_needed()
    page.click(f'{href_link}')

    pg_url = f'http://newonpan.getmall.kr/front/productsearch.php?block={page_idx}&gotopage={page_no}&sort=&codeA=&codeB=&codeC=&codeD=&minprice=&maxprice=&s_check=all&search={keyword}&search1=&listnum=20'    
    page.wait_for_url(url=pg_url, timeout=5000)    # working
    
''' Access each product in the page '''    
def get_page_products(page_no):    
    print(f'GET_PAGE_PRODUCTS.............PAGE:{page_no}')
    page = browser.page()  
    
    body_locator = browser.page().locator("//table/tbody/tr/td[*]/a/p.prname")
    locators = body_locator.all()     # empty list
    if locators.count == 0:
        print('LOCATORS is NULL')
    
    idx = 0        
    for loc in locators:
        # prname_loc = loc.locator('p.prname')
        pr_name = loc.text_content
        # print(f'PAGE:{page_no}, IDX:{idx}, {loc.type} ')
        print(f'PAGE:{page_no}, IDX:{idx}, {pr_name} ')
        idx = idx + 1

    idx = 0
    text_lists = body_locator.all_text_contents()
    if text_lists.count == 0:
        print('TEXT_LISTS is NULL')
    for text_content in text_lists:
        print(f'PAGE:{page_no}, IDX:{idx}, {text_content} ')
        idx = idx + 1
        
    # locators = body_locator.get_by_role('tr').all()
    # print(f"2.......... PAGE_NO:{page_no}, COUNT: {locators.index}")
    # for li in page.get_by_role('tbody').all():
    #     texts = li.all_inner_texts()
    #     for text in texts:
    #         print(f"3...........{text}")
    
                
''' Access each product in the page '''    
def get_page_products2(page_no):   
    print(f'GET_PAGE_PRODUCTS2.............PAGE:{page_no}') 
     # Get the locator for all product rows in the table
    product_rows = browser.page().locator('tbody tr')
    
    # Get the count of rows to loop through
    row_count = product_rows.count()
    print(f'\nPAGE:{page_no}, "tbody tr" 갯수: {row_count}')

    # Create a list to store the extracted data
    extracted_data = []

    for i in range(row_count):
        row = product_rows.nth(i)
        try:
            # Locate the href link within the current row
            href_link_locator = ''
            href_link = ''
            if row.locator('a[href*="productdetail.php"]').is_visible(timeout=500):
                href_link_locator = row.locator('a[href*="productdetail.php"]')
                href_link = href_link_locator.get_attribute("href", timeout=500)
            else:
                continue
            
            # Locate the prname text within the current row
            prname_locator = ''
            prname_text = ''
            if row.locator('p.prname').is_visible(timeout=500):
                prname_locator = row.locator('p.prname')
                prname_text = prname_locator.text_content()
                print(f"PG:{page_no}, IDX:{i}, prname: {prname_text}")
            else:
                continue
            
            # Store the data
            if href_link and prname_text:
                extracted_data.append({
                    "href": href_link,
                    "prname": prname_text.strip() # .strip() removes whitespace
                })

        except Exception as e:
            # Handle cases where a row might not contain the elements
            print(f"Skipping a row due to an error: {e}")
            continue

    print(f'PG:{page_no}, PROD: LEN:{len(extracted_data)}, DATA:{extracted_data}\n')
    return extracted_data