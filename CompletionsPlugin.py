import sublime, sublime_plugin
import Pywin32.setup
import win32com.client
import win32api
import os

settings_file = "StataEditor.sublime-settings"

def plugin_loaded():
    global settings
    settings = sublime.load_settings(settings_file)

class VariableCompletions(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if view.scope_name(view.sel()[0].a) != 'source.stata ':
			return
		else:
			if settings.get("variable_completions") == True:
				try:
					varlist = sublime.stata.VariableNameArray()
					complist = []
					for i in varlist:
						complist.append([i + "\tVariable",i])
					return complist
				except AttributeError:
					return
			else:
				return

class FunctionCompletions(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if view.scope_name(view.sel()[0].a) != 'source.stata ':
			return
		else:
			if settings.get("function_completions") == True:
				funclist = ["abs","acos","acosh","asin","asinh","atan","atan2","atanh","ceil","cloglog","comb","cos","cosh","digamma","exp","floor","int","invcloglog","invlogit","ln","lnfactorial","lngamma","log","log10","logit","max","min","mod","reldif","round","sign","sin","sinh","sqrt","sum","tan","tanh","trigamma","trunc","ibeta","betaden","ibetatail","invibeta","invibetatail","nibeta","nbetaden","invnibeta","binomial","binomialp","binomialtail","invbinomial","invbinomialtail","chi2","chi2den","chi2tail","invchi2","invchi2tail","nchi2","nchi2den","nchi2tail","invnchi2","invnchi2tail","npnchi2","dunnettprob","invdunnettprob","F","Fden","Ftail","invF","invFtail","nF","nFden","nFtail","invnFtail","npnF","gammap","gammaden","gammaptail","invgammap","invgammaptail","dgammapda","dgammapdada","dgammapdadx","dgammapdx","dgammapdxdx","hypergeometric","hypergeometricp","nbinomial","nbinomialp","nbinomialtail","invnbinomial","invnbinomialtail","binormal","normal","normalden","normalden","normalden","invnormal","lnnormal","lnnormalden","lnnormalden","lnnormalden","poisson","poissonp","poissontail","invpoisson","invpoissontail","t","tden","ttail","invt","invttail","nt","ntden","nttail","invnttail","npnt","tukeyprob","invtukeyprob","rbeta","rbinomial","rchi2","rgamma","rhypergeometric","rnbinomial","rnormal","rnormal","rpoisson","rt","abbrev","char","indexnot","itrim","length","lower","ltrim","plural","proper","real","regexm","regexr","regexs","reverse","rtrim","soundex","soundex_nara","strcat","strdup","string","string","strlen","strlower","strltrim","strmatch","strofreal","strofreal","strpos","strproper","strreverse","strrtrim","strtoname","strtoname","strtrim","strupper","subinstr","subinword","substr","trim","upper","word","wordcount","autocode","c","chop","clip","cond","e","fileexists","fileread","filereaderror","float","fmtwidth","has_eprop","inlist","inrange","irecode","matrix","mi","missing","r","recode","return","s","scalar","tin","twithin","tin","twithin","colnumb","colsof","det","diag0cnt","el","issymmetric","matmissing","mreldif","rownumb","rowsof","trace","cholesky","corr","diag","get","hadamard","I","inv","invsym","J","matuniform","nullmat","sweep","vec","vecdiag"]
				complist = []
				for i in funclist:
					complist.append([i + "\tFunction",i + "($1)$0"])
				return complist
			else:
				return

class CommandCompletions(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if view.scope_name(view.sel()[0].a) != 'source.stata ':
			return
		else:
			if settings.get("command_completions") == True:
				cmdlist = ["_assert_mreldif","_cassert","_check4gropts","_check_omit","_cmdxel","_coef_table","_coef_table_header","_confirm_date","_crcar1","_datasignature","_diparm","_estimates","_findhlpalias","_fv_check_depvar","_get_diopts","_get_diparmopts","_get_eformopts","_get_eqspec","_get_gropts","_get_offopt","_getcovcorr","_getfilename","_labels2names","_massert","_matplot","_mgarch_p_names","_mkcross","_mkvec","_ms_at_parse","_ms_balance","_ms_build_info","_ms_display","_ms_dydx_parse","_ms_element_info","_ms_empty_info","_ms_eq_display","_ms_eq_info","_ms_extract_varlist","_ms_findomitted","_ms_omit_info","_ms_op_info","_ms_parse_parts","_ms_put_omit","_ms_split","_ms_unab","_mtest","_natscale","_nobs","_on_colon_parse","_parse","_pred_se","_predict","_qreg","_qsort_index","_recast","_rename","_restore_labels","_return","_rmcoll","_rmcoll2list","_rmcollright","_robust","_sassert","_score_spec","_sep_varsylags","_strip_labels","_stubstar2names","_svy_mkdeff","_svy_mkmeff","_svy_setup","_ts","_tsnatscale","_vassert","_vce_parse","_vce_parserun","_xt","_xtstrbal","about","adjust","adoupdate","alpha","ameans","anova","anova_terms","anovadef","aorder","append","arch","areg","arfima","args","arima","asclogit","asmprobit","asroprobit","assert","bcal","binreg","biplot","biprobit","bitest","bitowt","boot","bootstrap","boxcox","break","brier","brrstat","bsample","bstat","by","ca","candisc","canon","capture","cc","cd","centile","cf","changeeol","char","chdir","checkdlgfiles","checkhlpfiles","checksum","chelp","ci","class","classutil","clear","clist","clogit","cloglog","clonevar","cls","cluster","cluster_stop","clustermat","cnreg","cnsreg","codebook","collapse","compare","compress","confirm","conren","constraint","continue","contract","contrast","copy","copyright","copysource","corc","corr2data","correlate","corrgram","count","cox","coxbase","creturn","cross","cs","cscript","cscript_log","ct","ctset","cttost","cumsp","cumul","cusum","datasignature","db","dbeta","deff","describe","destring","dfactor","dfgls","dfuller","di_g","dir","dirstats","discard","discrim","discrim_knn","discrim_lda","discrim_logistic","discrim_qda","disp_res","display","do","doedit","dotplot","dprobit","drawnorm","drop","ds","dstdize","dta_equal","dtaverify","dtaversion","duplicates","dvech","dydx","edit","egen","eivreg","encode","eq","erase","ereturn","error","esize","estat","estimates","estimates_notes","etpoisson","etregress","exit","exlogistic","expand","expandcl","expoisson","export","expr_query","factor","fcast","fcast_compute","fcast_graph","fdasave","file","filefilter","fillin","findfile","findit","fit","for","foreach","forecast","format","forvalues","fp","fracpoly","frontier","fvexpand","fvrevar","fvset","generate","genrank","getcmds","getcmds_personal","gettoken","glm","glogit","gmm","gphdot","gphprint","gprefs","graph","graph7","grebar","greigen","grmeanby","gs_fileinfo","gs_filetype","gs_graphinfo","gs_stat","gsort","h","hadimvo","hausman","haver","heckman","heckoprobit","heckprobit","help","hetprobit","hexdump","hilite","histogram","hotel","hreg","hsearch","icc","icd9","if","iis","import","import_delimited","import_excel","import_haver","impute","include","infile","infix","input","insheet","inspect","inten","intreg","ipolate","ir","irf","irf_create","is_svy","isid","ivpoisson","ivprobit","ivreg","ivregress","ivtobit","jackknife","javacall","jkstat","joinby","kappa","kdensity","ksm","ksmirnov","kwallis","label","labelbook","ladder","levels","levelsof","leverage","lfit","lincom","line","linktest","list","lnskew0","log","logistic","logit","loneway","lookfor","lookup","lowess","lpoly","lrecomp","lroc","lrtest","lsens","lstat","ltable","lv","macro","makecns","manova","margins","marginsplot","mark","mat_capp","mat_put_rr","mata","mata_clear","mata_describe","mata_drop","mata_matsave","mata_memory","mata_mlib","mata_mosave","mata_rename","mata_which","matalabel","matlist","matrix","mca","mcc","mds","mdslong","mdsmat","mdytoe","mean","means","mecloglog","meglm","melogit","memory","menbreg","meologit","meoprobit","mepoisson","meprobit","meqrlogit","meqrpoisson","merge","merge_10","mfp","mfx","mgarch","mgarch_ccc","mgarch_dcc","mgarch_dvech","mgarch_vcc","mhodds","mi","minbound","misstable","mixed","mkassert","mkdir","mkmat","mkspline","ml","ml_hold","ml_score","mleval","mlexp","mlogit","mlopts","more","mprobit","mvencode","mvreg","mvtest","nbreg","nestreg","net","newey","news","nl","nlcom","nlinit","nlogit","nlsur","notes","notes_dlg","novarabbrev","nptrend","numlist","odbc","ologit","ologitp","oneway","oprobit","opts_exclusive","order","orthog","outfile","outsheet","ovtest","palette","parse","parse_dissim","pause","pca","pcorr","pctile","pergram","permute","pkcollapse","pkcross","pkequiv","pkexamine","pkshape","pksumm","plot","plugin","poisgof","poisson","post","postrtoe","power","pperron","prais","predict","predictnl","preserve","print","probit","procrustes","profiler","program","projmanager","proportion","prtest","psdensity","putexcel","putmata","pwcompare","pwmean","qby","qreg","quadchk","query","quietly","range","ranksum","ratio","rcof","recast","recode","reg3","regress","remap","rename","renpfix","repeat","reshape","return","rmdir","roccomp","rocfit","rocreg","rocregplot","roctab","rolling","rologit","rotate","rotatemat","rreg","runtest","sample","sampsi","save","scalar","scatter","scobit","score","scoreplot","screeplot","sdtest","search","sem","sem_estat_eqgof","sem_estat_eqtest","sem_estat_framework","sem_estat_ggof","sem_estat_ginvariant","sem_estat_gof","sem_estat_mindices","sem_estat_residuals","sem_estat_scoretests","sem_estat_stable","sem_estat_stdize","sem_estat_teffects","separate","serrbar","serset","set_defaults","shell","signestimationsample","signrank","simulate","sktest","sleep","slogit","smooth","snapshot","snapspan","sort","spearman","spikeplot","split","ssc","ssd","sspace","st","st_is","stack","statsby","stbase","stci","stcox","stcrreg","stcstat","stcurve","stdescribe","stem","stepwise","stfill","stgen","stir","storedresults","stphtest","stpower","stptime","strate","streg","sts","stset","stsplit","stsum","sttocc","sttoct","stvary","stweib","suest","sum","summarize","sunflower","sureg","svar","svy","svy_estat","svydescribe","svygen","svymarkout","svymlog","svyopts","svyset","svytest","swcox","swilk","symmetry","syntax","sysdescribe","sysdir","sysuse","tabdisp","table","tabodds","tabstat","tabulate","teffects","test","testnl","teststd","tetrachoric","timer","tnbreg","tobit","tokenize","total","tpoisson","translate","treatreg","truncreg","tsappend","tsfill","tsfilter","tsline","tsreport","tsrevar","tsset","tssmooth","ttest","tutorial","twoway__function_gen","twoway__histogram_gen","twoway__kdensity_gen","type","ucm","unab","unabbrev","unabcmd","update","use","var","varbasic","varfcast","vargranger","varlmar","varmanage","varnorm","varsoc","varstable","varwle","vce","vec","veclmar","vecnorm","vecrank","vecstable","version","view","viewsource","vwls","webdescribe","webgetsem","webseek","webuse","which","while","wntestb","wntestq","xcorr","xi","xmlsave","xpose","xtabond","xtcloglog","xtcorr","xtdata","xtdescribe","xtdpd","xtdpdsys","xtfrontier","xtgee","xtgls","xthausman","xthtaylor","xtintreg","xtivreg","xtline","xtlogit","xtmelogit","xtmepoisson","xtmixed","xtnbreg","xtologit","xtoprobit","xtpcse","xtpoisson","xtprobit","xtrc","xtrchh","xtreg","xtregar","xtset","xtsum","xttab","xttobit","xtunitroot","zinb","zip","zipfile","ztnb","ztp"]
				complist = []
				for i in cmdlist:
					complist.append([i + "\tCommand",i])
				return complist
			else:
				return

class FileCompletions(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if view.scope_name(view.sel()[0].a) != 'source.stata ':
			return
		else:
			if settings.get("file_completions") != False:
				complist = []
				for i in sublime.file_list:
					complist.append([i + "\tfile", '"' + i + '"'])
				return complist
			else:
				return
