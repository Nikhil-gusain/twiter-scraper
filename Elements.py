class ElementsStr():

    #scrapping divs
    timeline = "//div[@aria-label='Timeline: Search timeline']"
    textinput = "text"
    usenameinput = "//input[@data-testid='ocfEnterTextTextInput']"
    passinput = "password"
    #functions
    getheight = "return document.body.scrollHeight"
    disttoscroll = "return document.body.scrollHeight - window.pageYOffset"
    #basic elements
    outerhtml = "outerHTML"

    #btn
    mailbtn = "//button[.//span[text()='Next']]"
    usernamebtn = "button[data-testid='ocfEnterTextNextButton']"
    loginbtn =  "//button[@data-testid='LoginForm_Login_Button' and not(@disabled)]"