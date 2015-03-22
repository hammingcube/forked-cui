'''

    Copyright (C) 2014 Codility Limited. <https://codility.com>

    This file is part of Candidate User Interface (CUI).

    CUI is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version accepted in a public statement
    by Codility Limited.

    CUI is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with CUI.  If not, see <http://www.gnu.org/licenses/>.

'''


from django.template.response import SimpleTemplateResponse
from django.conf import settings
from django.template.response import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

SERVER_UI_OPTIONS = {
        "ticket_id": "TICKET_ID",

        "time_elapsed_sec": 15,
        "time_remaining_sec": 1800,

        "current_human_lang": "en",
        "current_prg_lang": "c",
        "current_task_name": "task1",

        "task_names": ["task1", "task2", "task3"],

        "human_langs": {
            "en": {"name_in_itself": "English"},
            "cn": {"name_in_itself": "\u4e2d\u6587"},
        },
        "prg_langs": {
            "c": {"version": "C", "name": "C"},
            "sql": {"version": "SQL", "name": "SQL"},
            "cpp": {"version": "C++", "name": "C++"},
        },

        "show_survey": True,
        "show_help": False,
        "show_welcome": True,
        "sequential": False,
        "save_often": True,

        "urls": {
            "status": "/chk/status/",
            "get_task": "/bit/c/_get_task/",
            "submit_survey": "/surveys/_ajax_submit_candidate_survey/TICKET_ID/",
            "clock": "/chk/clock/",
            "close": "/c/close/TICKET_ID",
            "verify": "/chk/verify/",
            "save": "/chk/save/",
            "timeout_action": "/chk/timeout_action/",
            "final": "/chk/final/",
            "start_ticket": "/bit/c/_start/"
        },
    }

TASK_RESP = {
	"task_status": "open",
	"task_description": "Description: task1,en,c",
	"task_type": "algo",
	"solution_template": "",
	"current_solution": "",
	"example_input": "",
	"prg_lang_list": ["c", "cpp"],
	"human_lang_list": ["en", "cn"],
	"prg_lang": "c",
	"human_lang": "en"
}

XML_RESP = """<?xml version="1.0" encoding="UTF-8"?>
<response>
   <current_solution />
   <example_input />
   <human_lang>en</human_lang>
   <human_lang_list>
      <element>en</element>
      <element>cn</element>
   </human_lang_list>
   <prg_lang>c</prg_lang>
   <prg_lang_list>
      <element>c</element>
      <element>cpp</element>
   </prg_lang_list>
   <solution_template />
   <task_description>Description: task1,en,c</task_description>
   <task_status>open</task_status>
   <task_type>algo</task_type>
</response>"""

XML_RESP2 = """<response>
     <task_status>open</task_status>
     <task_description>Description: task1,en,c</task_description>
     <task_type>algo</task_type>
     <solution_template></solution_template>
     <current_solution></current_solution>
     <example_input></example_input>
     <prg_lang_list>[&#34;c&#34;,&#34;cpp&#34;]</prg_lang_list>
     <human_lang_list>[&#34;en&#34;,&#34;cn&#34;]</human_lang_list>
     <prg_lang>c</prg_lang>
     <human_lang>en</human_lang>
 </response>"""

def render_cui(context):
    context = context.copy()
    context['STATIC_URL'] = settings.STATIC_URL
    context['DEBUG'] = settings.DEBUG
    context['ticket'] = { 'id': 'TICKET_ID' }
    context['in_devel'] = True
    return SimpleTemplateResponse('cui/cui.html', context)


def cui_test(request):
    '''Scaffolding for candidate interface JS tests.'''

    return render_cui({
        'in_test': True,
        'title': 'CUI tests'
    })

def cui_local(request):
    '''Scaffolding for candidate interface with mock local server.'''

    return render_cui({
        'in_local': True,
        'title': 'BISCUIT',
    })

@csrf_exempt
def server_options(request):
	'''Server options.'''
	print("Here")
	return HttpResponse(json.dumps(SERVER_UI_OPTIONS))

@csrf_exempt
def bit_handler(request, cmd):
	print("In bit_handler, received {cmd}".format(cmd=cmd))
	if cmd == '_start':
		return HttpResponse(json.dumps({'started': 'OK'}), content_type="application/json")
	elif cmd == '_get_task':
		return  HttpResponse(XML_RESP2, content_type="text/xml; charset=utf-8")
	else:
		return HttpResponse("Not Found")

@csrf_exempt
def clock_handler(request):
	print('Clock handler called')
	return HttpResponse(json.dumps({
	"result": "OK",
	"new_timelimit": -1426973060
	}), content_type="application/json")
