Search.setIndex({docnames:["changelog","config","contask","extensions","fluent","fluent API","fluent.core","fluent.extensions","gevent","index","install","log","monitor","monitor_resource","quickstart","scheduler","thread_flex","\u5982\u4f55\u5199\u4e00\u4e2a\u63d2\u4ef6"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.todo":1,"sphinx.ext.viewcode":1,sphinx:54},filenames:["changelog.rst","config.rst","contask.rst","extensions.rst","fluent.rst","fluent API.rst","fluent.core.rst","fluent.extensions.rst","gevent.rst","index.rst","install.rst","log.rst","monitor.rst","monitor_resource.rst","quickstart.rst","scheduler.rst","thread_flex.rst","\u5982\u4f55\u5199\u4e00\u4e2a\u63d2\u4ef6.rst"],objects:{"":{fluent:[5,0,0,"-"]},"fluent.cli":{extract_worker_dir:[5,1,1,""],get_conf:[5,1,1,""],go:[5,1,1,""],load_module_after_init:[5,1,1,""]},"fluent.core":{inputer:[6,0,0,"-"],outputer:[6,0,0,"-"],processor:[6,0,0,"-"],utils:[6,0,0,"-"]},"fluent.core.inputer":{Inputer:[6,2,1,""]},"fluent.core.inputer.Inputer":{NAME:[6,3,1,""],exit_one_thread:[6,4,1,""],handle_item:[6,4,1,""],handle_item_result:[6,4,1,""],internal:[6,3,1,""],item_wrapper:[6,4,1,""],start:[6,4,1,""],start_threads:[6,4,1,""]},"fluent.core.outputer":{Outputer:[6,2,1,""]},"fluent.core.outputer.Outputer":{INTERVAL_DEFAULT:[6,3,1,""],NAME:[6,3,1,""],exit:[6,4,1,""],exit_one_thread:[6,4,1,""],handle_item:[6,4,1,""],start:[6,4,1,""],start_threads:[6,4,1,""]},"fluent.core.processor":{Processor:[6,2,1,""]},"fluent.core.processor.Processor":{NAME:[6,3,1,""],exit:[6,4,1,""],exit_one_thread:[6,4,1,""],item_wrapper:[6,4,1,""],put:[6,4,1,""],start:[6,4,1,""],start_threads:[6,4,1,""]},"fluent.core.utils":{CatchExceptionHandler:[6,2,1,""],ThreadSafe:[6,2,1,""],get_class:[6,1,1,""],import_by_abspath:[6,1,1,""],import_module:[6,1,1,""]},"fluent.core.utils.CatchExceptionHandler":{handle_item:[6,4,1,""],handle_item_debug:[6,4,1,""]},"fluent.core.utils.ThreadSafe":{EXIT_SIGNAL:[6,3,1,""],NAME:[6,3,1,""],exit:[6,4,1,""],is_flex_thread_alive:[6,4,1,""],report:[6,4,1,""],start:[6,4,1,""],start_one_thread:[6,4,1,""]},"fluent.extensions":{monitor:[7,0,0,"-"],monitor_resource:[7,0,0,"-"],thread_flex:[7,0,0,"-"]},"fluent.extensions.monitor":{InputQueueMonitor:[7,2,1,""],MonitorEnum:[7,2,1,""],MonitorQueue:[7,2,1,""],OutputQueueMonitor:[7,2,1,""]},"fluent.extensions.monitor.InputQueueMonitor":{NAME:[7,3,1,""]},"fluent.extensions.monitor.MonitorEnum":{in_counter:[7,3,1,""],out_counter:[7,3,1,""],used_rate:[7,3,1,""]},"fluent.extensions.monitor.MonitorQueue":{NAME:[7,3,1,""],in_counter:[7,4,1,""],out_counter:[7,4,1,""],used_rate:[7,4,1,""]},"fluent.extensions.monitor.OutputQueueMonitor":{NAME:[7,3,1,""]},"fluent.extensions.thread_flex":{FlexMethod:[7,2,1,""],FlowThreadNumberManager:[7,2,1,""],ThreadFlexQueue:[7,2,1,""]},"fluent.extensions.thread_flex.FlexMethod":{add:[7,3,1,""],reduce:[7,3,1,""]},"fluent.extensions.thread_flex.FlowThreadNumberManager":{add:[7,4,1,""],base_number:[7,3,1,""],collect_mem:[7,4,1,""],flex_step:[7,3,1,""],flow:[7,3,1,""],get_add_flex_step:[7,4,1,""],get_reduce_flex_step:[7,4,1,""],is_larger_than_base:[7,4,1,""],is_less_than_max_number:[7,4,1,""],reduce:[7,4,1,""]},"fluent.extensions.thread_flex.ThreadFlexQueue":{NAME:[7,3,1,""],is_higher_state:[7,4,1,""],is_lower_state:[7,4,1,""],used_rate:[7,4,1,""]},"fluent.log":{Logger:[5,2,1,""],set_logger:[5,1,1,""]},"fluent.log.Logger":{DEFAULT_BACKUP_COUNT:[5,3,1,""],DEFAULT_FORMAT:[5,3,1,""],DEFAULT_LEVEL:[5,3,1,""],DEFAULT_MAX_BYTES:[5,3,1,""],conf:[5,3,1,""],get_formater:[5,4,1,""],get_logger:[5,4,1,""],get_rotating_logger:[5,4,1,""],logging_conf:[5,3,1,""],replace_logging:[5,4,1,""],set_file:[5,4,1,""],set_format:[5,4,1,""],set_level:[5,4,1,""]},"fluent.model":{Config:[5,2,1,""],Extra:[5,2,1,""],FlowItem:[5,2,1,""]},"fluent.model.Config":{get:[5,4,1,""]},"fluent.model.Extra":{load_extra:[5,4,1,""]},"fluent.model.FlowItem":{extra:[5,4,1,""],inject:[5,4,1,""]},"fluent.reporter":{SendMonitorMessageException:[5,5,1,""],Telegraf:[5,2,1,""]},"fluent.reporter.Telegraf":{close:[5,4,1,""],report:[5,4,1,""],report_cost:[5,4,1,""],report_task_progress:[5,4,1,""],send:[5,4,1,""]},"fluent.scheduler":{Scheduler:[5,2,1,""]},"fluent.scheduler.Scheduler":{SETUP_ASIDE_FLOWS:[5,3,1,""],conf:[5,3,1,""],core_flows:[5,3,1,""],e:[5,3,1,""],exit:[5,4,1,""],init_aside_flows:[5,4,1,""],register_flow:[5,6,1,""],reporter:[5,3,1,""],set_signal:[5,4,1,""],start:[5,4,1,""],start_debug_mode:[5,4,1,""],start_flows_on_threads:[5,4,1,""],stop:[5,4,1,""],stop_aside_flows:[5,4,1,""]},fluent:{_global:[5,0,0,"-"],cli:[5,0,0,"-"],core:[6,0,0,"-"],extensions:[7,0,0,"-"],log:[5,0,0,"-"],model:[5,0,0,"-"],reporter:[5,0,0,"-"],scheduler:[5,0,0,"-"]}},objnames:{"0":["py","module","Python \u6a21\u5757"],"1":["py","function","Python \u51fd\u6570"],"2":["py","class","Python \u7c7b"],"3":["py","attribute","Python \u5c5e\u6027"],"4":["py","method","Python \u65b9\u6cd5"],"5":["py","exception","Python \u4f8b\u5916"],"6":["py","classmethod","Python \u7c7b\u65b9\u6cd5"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:attribute","4":"py:method","5":"py:exception","6":"py:classmethod"},terms:{"00":12,"001":6,"00z":12,"06":0,"10":[5,12],"100":[1,5],"10t23":12,"119":12,"120":12,"132434567000":5,"1570627595284236032":12,"1570627595284264960":12,"1570627596291826944":12,"1570627596291835904":12,"1570627597297064192":12,"1570627597297089024":12,"1570627598301306112":12,"1tkdb3kcnctqqcvtrw29q425a8yiqcqvdfxlesxmy01q":12,"20":[0,5],"2019":12,"2021":0,"223":12,"224":12,"339":12,"343":12,"459":12,"460":12,"500":5,"60":1,"class":[5,6,7,14,17],"default":[1,5],"for":7,"if":8,"import":[2,5,8,14],"int":6,"return":14,"true":1,"with":9,__init__:[14,17],_client:8,_extra:14,_global:[2,8,9,14],abc:5,abspath:6,activ:10,adb:5,add:7,add_job:2,alia:7,an:9,arg:[6,17],argv:6,asctim:5,attent:9,attribut:[6,17],base_numb:7,basicconf:5,be:0,begin:6,block:8,by:0,call:0,caption:12,catchexceptionhandl:6,changelog:9,check:10,child:6,cimpl:8,classmethod:5,cli:9,clone:10,close:5,cls:6,code:10,collect_mem:7,com:[10,12],command:10,conf:[5,6,17],config:[5,9,14],confluent:8,confluent_kafka:8,consum:[5,8],content:9,core:[9,14],core_flow:5,cost:5,cost_tim:5,counter:7,counterqueu:7,cpu:[1,3,17],creat:9,cron:2,cron_task:2,crontask:[3,5,9,14],ctrl:[5,14],dai:2,data:0,debug:[0,5],def:[14,17],default_backup_count:5,default_format:5,default_level:5,default_max_byt:5,dict:5,dir:6,directori:[5,6],doc:12,document:[10,12],domain:5,done:7,easi:0,edit:12,els:8,env:14,environ:10,etl:[4,6,7],event:5,except:[0,5,6],exit:[5,6],exit_one_thread:6,exit_sign:[6,17],extens:9,extension_nam:5,extensionabc:17,extra:[5,14],extra_str:5,extract_worker_dir:5,fals:[1,5,6,17],father_span:6,field:[5,7,12],filehandl:5,filenam:[5,6],filepath:5,find:6,flask:10,flex_max_r:7,flex_step:7,flex_step_r:7,flexmethod:7,flow:[5,7],flow_item:6,flow_typ:5,flowitem:5,flowthreadnumbermanag:7,fluent:[1,2,8,14],fluent_log:1,fluent_queu:1,follow:10,format:5,from:[2,8,12,14],func:0,funcnam:5,get:[0,5,9,12],get_add_flex_step:7,get_class:6,get_conf:5,get_format:5,get_logg:5,get_reduce_flex_step:7,get_rotating_logg:5,getlogg:5,gevent:[1,9],git:10,github:12,go:[5,10],googl:12,grafana:9,greenlet:8,gvent:8,handle_item:[6,14],handle_item_debug:6,handle_item_result:6,handler:5,happen:0,host:5,hour:2,http:[10,12],import_by_abspath:6,import_modul:6,in_count:[7,12],influx:12,influxdata:12,influxdb:[1,5,9],info:5,init_aside_flow:5,inject:5,input:[0,1,5,14],input_item:17,input_q:[7,12],input_q_s:1,inputqueuemonitor:7,instal:9,int_q:6,intern:6,interv:[1,5],interval_default:6,io:1,is:10,is_flex_thread_al:6,is_higher_st:7,is_larger_than_bas:7,is_less_than_max_numb:7,is_lower_st:7,it:0,item:[5,6],item_wrapp:6,job:[5,6,9,12],job_dir:5,joox_cms_backend:5,json_bodi:12,kafka:8,kafka_timeout:8,kafkaerror:8,kill:[5,14],kwarg:6,latest:10,level:5,levelnam:5,lib:8,limit:12,line:5,lineno:5,list:5,load_extra:5,load_module_after_init:5,log:[0,1,9],logger:5,logging_conf:5,loop:1,ls:14,max_numb:7,measur:[1,5,12],mem:1,messag:5,method:5,mode:0,model:9,modul:9,modulenotfounderror:6,monitor:[1,3,5,9],monitor_resourc:[1,3,5,9,17],monitorenum:7,monitorqueu:7,monitorresourc:[5,17],monkei:8,month:2,msg:8,name:[5,6,7,12,14],none:5,not:[0,6],now:10,number:7,oa:10,object:[5,6],of:[5,6,10],or:[10,14],out:10,out_count:[7,12],out_q:6,output:[0,5,14],output_q:[7,12],output_q_s:1,outputqueuemonitor:7,overview:[9,10],parent_class:6,patch:8,pid:14,pip:10,pipe:0,poll:8,pre_tag:5,process:[0,5,7,14],processnam:5,processor:5,produc:5,project:14,properti:5,put:[6,12],py:[2,14],python:[9,12],queue:[6,7],quickstart:[9,10],rais:6,recommend:10,reduc:7,register_flow:[5,17],releas:0,replace_log:5,report:[1,6,9],report_cost:5,report_str:5,report_task_progress:5,reset_modify_tim:2,result:5,rlock:6,rotatefilehandl:5,schedul:[1,6,9,17],select:12,self:[8,14,17],send:5,sendmonitormessageexcept:5,servic:5,set_fil:5,set_format:5,set_level:5,set_logg:5,set_sign:5,setup_aside_flow:5,shuffler:5,signalnum:5,sleep:8,socket:8,span:5,span_format_typ:5,stack:0,start:[5,6,9],start_debug_mod:5,start_flows_on_thread:5,start_one_thread:6,start_thread:6,stop:[5,14],stop_aside_flow:5,str:[5,6],submodul:5,success:5,supervisorctl:14,support:0,tag:[5,12],task_dir:5,task_nam:[5,12],telegraf:[1,5,9],templat:9,term:5,test:[12,14],text_map:5,the:[9,10],then:9,thread:1,thread_flex:[1,3,5,9],thread_nam:6,threadflex:5,threadflexqueu:7,threading_count:6,threadnam:5,threadsaf:6,time:12,timeout:6,to:[0,10],todo:7,tps:1,transfer:0,trigger:2,tupl:[5,7],type:6,use:10,used_r:[7,12],userinput:14,using:10,util:[5,8],valu:[5,6],version:9,we:10,when:0,will:0,within:10,worker:5,yaml:14,year:2,yoyoyo:10},titles:["Changelog","config\u6587\u4ef6\u7684\u4f7f\u7528\u65b9\u5f0f","crontask","extensions","fluent","fluent API","fluent.core API","fluent.extensions API","gevent","Welcome to Fluent\u2019s documentation!","Install fluent","fluent log \u8bbe\u8ba1\u539f\u5219","monitor","monitor_resource","quickstart","scheduler","thread_flex","\u5982\u4f55\u5199\u4e00\u4e2a\u63d2\u4ef6"],titleterms:{"with":14,_global:5,and:9,api:[5,6,7,9],attent:14,changelog:0,cli:5,config:1,content:[5,6,7],core:[5,6],creat:14,crontask:2,document:9,extens:[3,5,7],fluent:[4,5,6,7,9,10,11],gevent:8,grafana:12,indic:9,influxdb:12,input:6,instal:10,job:14,log:[5,11],model:5,modul:[5,6,7],monitor:[7,12],monitor_resourc:[7,13],output:6,processor:6,python:10,quickstart:14,report:5,schedul:[5,15],start:14,submodul:6,tabl:9,telegraf:12,templat:14,thread_flex:[7,16],to:9,util:6,version:[0,10],welcom:9}})