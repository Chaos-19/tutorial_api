import subprocess
from html_to_markdown import convert_to_markdown
from pygments.lexers import guess_lexer, ClassNotFound
from pygments.formatters import HtmlFormatter
from bs4.element import Tag
import logging
import mdformat 
import re



'''
class NodeLangDetector:
    def __init__(self, path_to_js):
        self.process = subprocess.Popen(
            ["node", path_to_js],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
    
    def detect(self, text):
        try:
            self.process.stdin.write(f"{text}\n")
            self.process.stdin.flush()
            return self.process.stdout.readline().strip()
        except Exception as e:
            logging.error(f"Error in NodeLangDetector: {str(e)}")
            return ""
    
    def close(self):
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait()
'''

import requests

def run_node_script(text):
    try:
        response = requests.post("http://localhost:3000", data=text)
        return response.text.strip()
    except Exception as e:
        return "javascript"

def code_b(*, tag: Tag, text: str,**kwargs):
    language = run_node_script(text)
    print(f"{language=}")
    code_lang = language.lower() if language.lower() in ["html", "css","javascript", "java"] else "java"
    print(f"{code_lang=}")
    return f'```{code_lang}\n{text}\n```\n'

def html_to_markdown(html):
    try:
        if html == "":
            return ""
            
        markdown = convert_to_markdown(
            html,
            wrap=True,
            wrap_width=100,
            custom_converters={"pre":code_b}
        )
        return markdown
    finally:
        print("finished")
        
def format_md(unformatted):
    unformatted = re.sub(r"\\", "", unformatted)
    if unformatted == "":
        return ""
        
    formatted = mdformat.text(unformatted)
    return formatted        
        
'''
from html_to_markdown import convert_to_markdown
from pygments.lexers import guess_lexer, ClassNotFound
from pygments.formatters import HtmlFormatter
from bs4.element import Tag
import subprocess

def run_node_script(path_to_js,arg):
    try:
        result = subprocess.run(["node", path_to_js,arg], capture_output=True, text=True)
        if result.stdout:
            return result.stdout
        if result.stderr:
            return result.stderr
    except Exception as e:       
        return "result.stdout"



def code_b(*, tag: Tag, text: str, **kwargs):
    language = run_node_script("./../../../nodejs_dir/test_pro/index.js",text).strip()
    print(f"{language=}")
    code_lang = language.lower() if language.lower() in ["html","javascript","typescript"] else "javascript"
    
    print(f"{code_lang=}")        
    return f'```{code_lang}\n{text}\n```\n'


def html_to_markdown(html):
    #formatter = HtmlFormatter(nowrap=True)  #
    markdown = convert_to_markdown(
                html,
                wrap=True, # Enable text wrapping 
                wrap_width=100, # Set wrap width
                custom_converters={"pre":code_b}
    )
    
    return markdown
'''