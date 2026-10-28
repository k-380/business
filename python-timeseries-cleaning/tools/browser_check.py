"""Optional authoring QA. Requires playwright==1.51.0 and its Chromium."""
from pathlib import Path
import json,tempfile
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

def main():
    errors=[]; requests=[];checks=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
        context=browser.new_context(viewport={'width':1280,'height':900})
        context.route('http://**',lambda r:r.abort());context.route('https://**',lambda r:r.abort())
        page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
        pages=['index.html','getting-started.html','labs.html','downloads.html','glossary.html','verification.html','datasets.html','implementation.html','references/bibliography.html']+[f'chapters/chapter{i:02d}.html' for i in range(1,25)]+['single-file.html']
        for width in [1280,390]:
            page.set_viewport_size({'width':width,'height':900})
            for path in pages:
                page.goto((ROOT/path).as_uri());page.wait_for_load_state('load')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,path,'horizontal overflow')
                assert page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)'),path
                checks.append({'path':path,'width':width,'layout':'pass'})
        page.goto((ROOT/'chapters/chapter11.html').as_uri())
        page.get_by_role('button',name='全文検索',exact=True).click()
        page.get_by_label('全24章・補講を検索（複数語はスペースで区切る）').fill('MAD')
        assert page.locator('#search-results .result').count()>0
        page.keyboard.press('Escape')
        details=page.locator('details.answers');assert not details.get_attribute('open')
        details.locator('summary').click();assert details.evaluate('(d)=>d.open')
        page.locator('button.copy').first.click();page.wait_for_function("document.querySelector('button.copy').textContent.includes('コピーしました')")
        page.get_by_role('button',name='明暗切替',exact=True).click()
        assert page.locator('html').get_attribute('data-theme')=='dark'
        screenshot_dir=Path(tempfile.gettempdir())/'tsclean-browser-qa';screenshot_dir.mkdir(exist_ok=True)
        page.screenshot(path=str(screenshot_dir/'chapter11-mobile.png'),full_page=False)
        page.goto((ROOT/'index.html').as_uri());page.set_viewport_size({'width':1280,'height':900})
        page.get_by_role('button',name='明暗切替',exact=True).click()
        page.screenshot(path=str(screenshot_dir/'cover-desktop.png'),full_page=False)
        page.goto((ROOT/'chapters/chapter16.html').as_uri())
        page.locator('#fig16').scroll_into_view_if_needed()
        page.screenshot(path=str(screenshot_dir/'chapter16-figure.png'),full_page=False)
        page.goto((ROOT/'single-file.html').as_uri())
        printpath=screenshot_dir/'single-file-print.pdf'
        page.pdf(path=str(printpath),format='A4',print_background=True,prefer_css_page_size=True)
        from pypdf import PdfReader
        pdf=PdfReader(printpath);pages_n=len(pdf.pages)
        import re,unicodedata
        text=re.sub(r'\s+','',unicodedata.normalize('NFKC','\n'.join(x.extract_text() or '' for x in pdf.pages)))
        assert all(c in text for c in ['第1章','第24章','演習解答']), 'print content'
        assert not errors,errors
        assert not requests,requests
        result={'browser':browser.version,'offline':True,'page_layout_checks':len(checks),'widths':[1280,390],'javascript_errors':errors,'external_requests':requests,'search':'pass','answer_toggle':'pass','copy_file_protocol':'pass','dark_mode':'pass','print_pages_A4':pages_n,'print_text_checks':'pass','screenshots_internal':str(screenshot_dir),'details':checks}
        (ROOT/'tests/browser-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='details'},ensure_ascii=False,indent=2))
        browser.close()
if __name__=='__main__':main()
