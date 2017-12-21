from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import re
from .helper import check, bn_char_pattern,  bn_al_pattern
from django.conf import settings
from bs4 import BeautifulSoup
import json

def index(request):
	
	return render(request, 'index.html')

@csrf_exempt
def spell_check_result(request):
	if request.method == 'POST':
		text = request.POST['text']
		# print(text)
		words = re.split(bn_char_pattern,  text)
		separators = re.split(bn_al_pattern, text)
		separators = list(filter(None, separators))
		i = 0
		text = ""
		total_word = len(words)
		total_error = 0
		num_nonw = 0
		for isNonWord, suggestions in check(words):
			word = words[i]
			if suggestions is not None:
				total_error += 1
				tds = ""
				for suggestion in suggestions:
					tds += '<tr><td class="suggest_op" >'+suggestion+'</td></tr>'

				high_light = "word-highlight-rw"	
				if isNonWord:
					num_nonw += 1
					high_light = "word-highlight-nw"

				word = """
    <a href="javascript:void(0)" onclick="open_suggestion_window(this)" class="word-link">
        <span class='"""+high_light+"""'>"""+ word +"""</span>
    </a>

    <div class="suggestion_window">
        <table class="suggest_tab">
            <tbody>
            """+ tds +"""
            </tbody>
        </table>
        <hr id="hr_divider">
        <a href="javascript:void(0)" onclick="ignore_suggest(this)" id="ignore_link">Ignore</a>
        <a href="javascript:void(0)" onclick="revert(this)" id="revert_link" hidden>Revert to 
        	 <span class='"""+high_light+"""'>"""+ word +"""</span></a><br>
        <a href="javascript:void(0)" onclick="close_window()" class="pull-right">Close</a>
    </div>                    

"""
			text += word
			if i < len(separators):
				text += separators[i]

			i += 1

		result_text = text 
		result_info = """
			<ul>
                <li>Total words processed: <span id="num_tot">"""+ str(total_word) +"""</span></li>
                <li>Total error found: <span id="num_err">"""+ str(total_error) +"""</span></li>
               	<li>Non word error: <span id="num_nonw">"""+ str(num_nonw) +"""</span></li>
                <li>Real word error: <span id="num_rw">"""+ str(total_error - num_nonw) +"""</span></li>
            </ul>
		"""
		response_data = {"result_text": result_text, "result_info": result_info}
		return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def edit_text(request):
	if request.method == 'POST':
		soup = BeautifulSoup(request.POST['text'], "html.parser")
		for span in soup.find_all('span'):
			span.unwrap()
		for a in soup.find_all('a'):
			a.unwrap()

		for div in soup.find_all('div', {'class': 'suggestion_window'}):
			div.decompose()

		return HttpResponse(soup)






