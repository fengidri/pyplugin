import os
wbcpickle = os.path.join(os.path.dirname(__file__), 'wbtree.cpickle').replace('\\','/')
wbtxt = os.path.join(os.path.dirname(__file__), 'wubi.txt').replace('\\','/')
fa_rule = """

>*
    *            base
    String       wubi

>c,cpp,python,javascript,ch,vim
    *            code
    CCommentDesc wubi
    CCommentArg  wubi
    Constant     wubi
    Comment      wubi
    String       wubi

>html
    *            wubi
    String       wubi
    cssStyle     code
    Statement    code
    Function     html
    Type         code
>context
    *            wubi
    Identifier   code
    Statement    code
>svn,gitcommit,markdown
    *            wubi

"""
