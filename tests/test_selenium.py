import pytest
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep

"""
Research Position Reference: 
https://careers.insidehighered.com/job/2251034/research-assistant-or-associate/
https://careers.insidehighered.com/job/2181701/postdoctoral-research-associate
"""
# User fixure
@pytest.fixture
def user1():
    return  {'email':'arslanay@wsu.edu', 'password':'strongpassword','passwor2':'strongpassword','id':'0116','status':'student'}

# User fixure
@pytest.fixture
def user2():
    return  {'email':'john@wsu.edu', 'password':'alsostrongpassword','id':'0117','status':'student'}

# User fixures
@pytest.fixture
def user2():
    return  {'email':'john@wsu.edu', 'password':'alsostrongpassword','id':'0118','status':'student'}

 # Post fixure
@pytest.fixture
def position1():
    return {'firstname':'Sakire',
            'lastname':'Arslan ',
            'phone_number':5093354089,
            'title': 'TA', 
            'project_information': 'Grade Students work' , 
            'start_date': "1/20",
            'end_date': "2/20",
            'required_time_commitment': "7",
            'required_gpa': "3.5",
            'required_course': "CptS322",
            'max_position': "5"}

 # Post fixure
@pytest.fixture
def position2():
    return {'firstname':'A',
            'lastname':'B ',
            'phone_number':123456,
            'title': 'Research Assistant', 
            'project_information': """This position will work closely with our multidisciplinary team of scientists to conduct research with 
                                    a primary focus on improving health in Native, rural, and other underserved populations. The successful 
                                    candidate’s personal research focus is flexible but must relate in some way to advancing public health, 
                                    population science, or reducing health disparities in our priority populations. Specific areas of need 
                                    within IREACH include advanced quantitative research methods and study design; neuroepidemiology 
                                    (including cognitive function, Alzheimer’s disease and related dementias, and brain imaging); social 
                                    epidemiology; practice-based research, food sovereignty and food systems, biomarkers for disease 
                                    susceptibility and trajectory; and implementation science. The expectation is that the successful 
                                    candidate will obtain funding and conduct research broadly related to one of the above areas. However, 
                                    individuals with other research interests relevant to the IREACH mission are encouraged to apply.""" , 
            'start_date': "2/20",
            'end_date': "3/20",
            'required_time_commitment': "15",
            'required_gpa': "3.6",
            'required_course': "CptS355",
            'max_position': "6"}

 # Post fixure
@pytest.fixture
def position3():
    return {'firstname':'C',
            'lastname':'D',
            'phone_number':67890,
            'title': 'Postdoctoral Research Associate', 
            'project_information': """The Postdoctoral Research Associate will use a multidisciplinary approach to integrate bacteriology, 
                                    molecular biology, genomics and microbiome research to (i) study pathogenicity and antimicrobial 
                                    resistance in food-borne pathogens such as Salmonella and (ii) discover causative agent and transmission 
                                    dynamics of elk hoof disease in the pacific northwest. As such successful candidates will need to have 
                                    demonstrated experience in conducting bacterial genomics and microbiome research with skills in basic and 
                                    molecular bacteriology, and next generation sequencing (NGS) data analysis. The Postdoctoral Research 
                                    Associate will perform experimental research directly relevant to the overall programmatic goals of the 
                                    laboratory. The incumbent must be capable of independent work but must also work well in a team environment. 
                                    Specific duties include, but are not limited to, designing and completing experiments in consultation with 
                                    the PI, performing basic and molecular bacteriological assays, and establish new assays to suit the needs of 
                                    the project. The Postdoctoral Research Associate will collect, organize and analyze bacteriological, microbiome 
                                    and NGS data, record data in laboratory notebooks, prepare scientific manuscripts, assist colleagues in the 
                                    laboratory and in day-to-day maintenance of laboratory function. Basic understanding of the relevant literature 
                                    and participation in weekly lab meetings is required.""" , 
            'start_date': "1/20",
            'end_date': "12/20",
            'required_time_commitment': "20",
            'required_gpa': "3.7",
            'required_course': "CptS350",
            'max_position': "7"}


"""
Download the chrome driver and make sure you have chromedriver executable in your PATH variable. 
To download the ChromeDriver to your system navigate to its download page. 
https://sites.google.com/a/chromium.org/chromedriver/home 
"""
@pytest.fixture
def browser():
    CHROME_PATH = "c:\\Webdriver"
    print(CHROME_PATH)
    opts = Options()
    opts.headless = False
    driver = webdriver.Chrome(options=opts, executable_path = CHROME_PATH + '\chromedriver.exe')
    driver.implicitly_wait(10)
    
    yield driver

    # For cleanup, quit the driver
    driver.quit()


def test_register_form(browser,user2):
    # test_user_1 = {'email':'arslanay@wsu.edu', 'password':'strongpassword','id':'0116','status':'student'}

    browser.get('http://localhost:5000/register')
    # Enable this to maximize the window
    # browser.maximize_window()

    browser.find_element_by_name("email").send_keys(user2['email'])
    sleep(2)
    browser.find_element_by_name("password").send_keys(user2['password'])
    sleep(2)
    browser.find_element_by_name("password2").send_keys(user2['password'])   
    sleep(2)  
    browser.find_element_by_name("id").send_keys(user2['id'])   
    sleep(2)  
    browser.find_element_by_name("status").send_keys(user2['status'])   
    sleep(2)  
    browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered user!' in content

def test_register_error(browser,user2):
    browser.get('http://localhost:5000/register')
    browser.find_element_by_name("email").send_keys(user2['email'])
    sleep(2)
    browser.find_element_by_name("password").send_keys(user2['password'])
    sleep(2)
    browser.find_element_by_name("password2").send_keys(user2['password'])    
    sleep(2)
    browser.find_element_by_name("id").send_keys(user2['id'])   
    sleep(2)  
    browser.find_element_by_name("status").send_keys(user2['status'])   
    sleep(2)  
    browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert 'Register' in content
    assert '[Please use a different email.]' in content

def test_login_form(browser,user2):
    browser.get('http://localhost:5000/login')
    browser.find_element_by_name("email").send_keys(user2['email'])
    sleep(2)
    browser.find_element_by_name("password").send_keys(user2['password'])
    sleep(2)
    browser.find_element_by_name("remember_me").click()
    sleep(2)
    button = browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert 'Welcome to Smile Portal!' in content
    assert user2['email'] in content

def test_invalidlogin(browser,user2):
    browser.get('http://localhost:5000/login')
    browser.find_element_by_name("email").send_keys(user2['email'])
    sleep(2)
    browser.find_element_by_name("password").send_keys('wrongpassword')
    sleep(2)
    browser.find_element_by_name("remember_me").click()
    sleep(2)
    browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert 'Invalid email or password' in content
    assert 'Sign In' in content

def test_post_smile(browser,user2,post1):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element_by_name("email").send_keys(user2['email'])
    browser.find_element_by_name("password").send_keys(user2['password'])
    browser.find_element_by_name("remember_me").click()
    browser.find_element_by_name("submit").click()

#     browser.get('http://localhost:5000/postsmile')
#     browser.find_element_by_name("title").send_keys(post1['title'])
#     sleep(2)
#     browser.find_element_by_name("body").send_keys(post1['body'])
#     sleep(2)
#     Select(browser.find_element_by_name("happiness_level")).select_by_visible_text(post1['happiness_level'])
#     sleep(2)
#     tags = browser.find_element_by_name("tag").click()
#     sleep(2)
#     browser.find_element_by_name("submit").click()
#     sleep(5)
#     #verification
#     content = browser.page_source
#     assert post1['title'] in content
#     assert post1['body'] in content

# def post_smile2(browser,user2,post2):
#     #first login
#     browser.get('http://localhost:5000/login')
#     browser.find_element_by_name("username").send_keys(user2['username'])
#     browser.find_element_by_name("password").send_keys(user2['password'])
#     browser.find_element_by_name("remember_me").click()
#     browser.find_element_by_name("submit").click()

#     browser.get('http://localhost:5000/postsmile')
#     browser.find_element_by_name("title").send_keys(post2['title'])
#     sleep(2)
#     browser.find_element_by_name("body").send_keys(post2['body'])
#     sleep(2)
#     Select(browser.find_element_by_name("happiness_level")).select_by_visible_text(post2['happiness_level'])
#     sleep(2)
#     tags = browser.find_element_by_name("tag").click()
#     sleep(2)
#     browser.find_element_by_name("submit").click()
#     sleep(5)
#     #verification
#     content = browser.page_source
#     assert post2['title'] in content
#     assert post2['body'] in content

# def test_post_smile_error(browser,user2,post3):
#     #first login
#     browser.get('http://localhost:5000/login')
#     browser.find_element_by_name("username").send_keys(user2['username'])
#     browser.find_element_by_name("password").send_keys(user2['password'])
#     browser.find_element_by_name("remember_me").click()
#     browser.find_element_by_name("submit").click()

#     browser.get('http://localhost:5000/postsmile')
#     browser.find_element_by_name("title").send_keys(post3['title'])
#     sleep(2)
#     browser.find_element_by_name("body").send_keys(post3['body'])
#     sleep(2)
#     Select(browser.find_element_by_name("happiness_level")).select_by_visible_text(post3['happiness_level'])
#     sleep(2)
#     tags = browser.find_element_by_name("tag").click()
#     sleep(2)
#     browser.find_element_by_name("submit").click()
#     sleep(10)
#     #verification
#     content = browser.page_source
#     assert "[Field must be between 1 and 1500 characters long.]" in content


if __name__ == "__main__":
    retcode = pytest.main()