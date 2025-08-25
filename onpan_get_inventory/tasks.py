import time
import re
from urllib.parse import quote
from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF


# from RPA.Browser.Selenium import Browser

keyword = "0"        #   "0"           #   "안전"

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
    # get_all_product_list()
    get_product_stock()
    
    

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
        # go to next page
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