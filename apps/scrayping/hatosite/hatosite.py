import time, csv,tqdm
import sys, os
import bs4, requests
import pandas as pd
from pprint import pprint
# res = requests.get('https://www.hatomarksite.com/search/zentaku/agent/area/#!pref=01')
# print(res.text)
# res = requests.get('https://www.hatomarksite.com/search/zentaku/agent/area/#!pref=01&syz=01101')
# print(res.text)

 # KYOUKAI_IDENT = {
# 'zentaku':'000','hokkaido':'001','aomori':'002','iwate':'003','miyagi':'004','akita':'005','yamagata':'006','fukushima':'007','ibaraki':'008','tochigi':'009','gunma':'010','saitama':'011','chiba':'012','tokyo':'013','kanagawa':'014','niigata':'015','toyama':'016','ishikawa':'017','fukui':'018','yamanashi':'019','nagano':'020','gifu':'021','shizuoka':'022','aichi':'023','mie':'024','shiga':'025','kyoto':'026','osaka':'027','hyogo':'028','nara':'029','wakayama':'030','tottori':'031','shimane':'032','okayama':'033','hiroshima':'034','yamaguchi':'035','tokushima':'036','kagawa':'037','ehime':'038','kochi':'039','fukuoka':'040','saga':'041','nagasaki':'042','kumamoto':'043','oita':'044','miyazaki':'045','kagoshima':'046','okinawa':'047'}

siku_code = [
    ['01101', '01102', '01103', '01104', '01105', '01106', '01107', '01108', '01109', '01110', '01202', '01203', '01204', '01205', '01206', '01207', '01208', '01209', '01210', '01211', '01212', '01213', '01214', '01215', '01216', '01217', '01218', '01219', '01220', '01221', '01222', '01223', '01224', '01225', '01226', '01227', '01228', '01229', '01230', '01231', '01233', '01234', '01235', '01236', '01303', '01304', '01331', '01332', '01333', '01334', '01337', '01343', '01345', '01346', '01347', '01361', '01362', '01363', '01364', '01367', '01370', '01371', '01391', '01392', '01393', '01394', '01395', '01396', '01397', '01398', '01399', '01400', '01401', '01402', '01403', '01404', '01405', '01406', '01407', '01408', '01409', '01423', '01424', '01425', '01427', '01428', '01429', '01430', '01431', '01432', '01433', '01434', '01436', '01437', '01438', '01452', '01453', '01454', '01455', '01456', '01457', '01458', '01459', '01460', '01461', '01462', '01463', '01464', '01465', '01468', '01469', '01470', '01471', '01472', '01481', '01482', '01483', '01484', '01485', '01486', '01487', '01511', '01512', '01513', '01514', '01516', '01517', '01518', '01519', '01520', '01543', '01544', '01545', '01546', '01547', '01549', '01550', '01552', '01555', '01559', '01560', '01561', '01562', '01563', '01564', '01571', '01575', '01578', '01581', '01584', '01585', '01586', '01601', '01602', '01604', '01607', '01608', '01609', '01610', '01631', '01632', '01633', '01634', '01635', '01636', '01637', '01638', '01639', '01641', '01642', '01643', '01644', '01645', '01646', '01647', '01648', '01649', '01661', '01662', '01663', '01664', '01665', '01667', '01668', '01691', '01692', '01693', '01694'],
    ['02201', '02202', '02203', '02204', '02205', '02206', '02207', '02208', '02209', '02210', '02301', '02303', '02304', '02307', '02321', '02323', '02343', '02361', '02362', '02367', '02381', '02384', '02387', '02401', '02402', '02405', '02406', '02408', '02411', '02412', '02423', '02424', '02425', '02426', '02441', '02442', '02443', '02445', '02446', '02450'],
    ['03201', '03202', '03203', '03205', '03206', '03207', '03208', '03209', '03210', '03211', '03213', '03214', '03215', '03216', '03301', '03302', '03303', '03321', '03322', '03366', '03381', '03402', '03441', '03461', '03482', '03483', '03484', '03485', '03501', '03503', '03506', '03507', '03524'],
    ['04101', '04102', '04103', '04104', '04105', '04202', '04203', '04205', '04206', '04207', '04208', '04209', '04211', '04212', '04213', '04214', '04215', '04216', '04301', '04302', '04321', '04322', '04323', '04324', '04341', '04361', '04362', '04401', '04404', '04406', '04421', '04422', '04424', '04444', '04445', '04501', '04505', '04581', '04606'],
    ['05201', '05202', '05203', '05204', '05206', '05207', '05209', '05210', '05211', '05212', '05213', '05214', '05215', '05303', '05327', '05346', '05348', '05349', '05361', '05363', '05366', '05368', '05434', '05463', '05464'],
    ['06201', '06202', '06203', '06204', '06205', '06206', '06207', '06208', '06209', '06210', '06211', '06212', '06213', '06301', '06302', '06321', '06322', '06323', '06324', '06341', '06361', '06362', '06363', '06364', '06365', '06366', '06367', '06381', '06382', '06401', '06402', '06403', '06426', '06428', '06461'],
    ['07201', '07202', '07203', '07204', '07205', '07207', '07208', '07209', '07210', '07211', '07212', '07213', '07214', '07301', '07303', '07308', '07322', '07342', '07344', '07362', '07364', '07367', '07368', '07402', '07405', '07407', '07408', '07421', '07422', '07423', '07444', '07445', '07446', '07447', '07461', '07464', '07465', '07466', '07481', '07482', '07483', '07484', '07501', '07502', '07503', '07504', '07505', '07521', '07522', '07541', '07542', '07543', '07544', '07545', '07546', '07547', '07548', '07561', '07564'],
    ['08201', '08202', '08203', '08204', '08205', '08207', '08208', '08210', '08211', '08212', '08214', '08215', '08216', '08217', '08219', '08220', '08221', '08222', '08223', '08224', '08225', '08226', '08227', '08228', '08229', '08230', '08231', '08232', '08233', '08234', '08235', '08236', '08302', '08309', '08310', '08341', '08364', '08442', '08443', '08447', '08521', '08542', '08546', '08564'],
    ['09201', '09202', '09203', '09204', '09205', '09206', '09208', '09209', '09210', '09211', '09213', '09214', '09215', '09216', '09301', '09342', '09343', '09344', '09345', '09361', '09364', '09384', '09386', '09407', '09411'],
    ['10201', '10202', '10203', '10204', '10205', '10206', '10207', '10208', '10209', '10210', '10211', '10212', '10344', '10345', '10366', '10367', '10382', '10383', '10384', '10421', '10424', '10425', '10426', '10428', '10429', '10443', '10444', '10448', '10449', '10464', '10521', '10522', '10523', '10524', '10525'],
    ['11101', '11102', '11103', '11104', '11105', '11106', '11107', '11108', '11109', '11110', '11201', '11202', '11203', '11206', '11207', '11208', '11209', '11210', '11211', '11212', '11214', '11215', '11216', '11217', '11218', '11219', '11221', '11222', '11223', '11224', '11225', '11227', '11228', '11229', '11230', '11231', '11232', '11233', '11234', '11235', '11237', '11238', '11239', '11240', '11241', '11242', '11243', '11245', '11246', '11301', '11324', '11326', '11327', '11341', '11342', '11343', '11346', '11347', '11348', '11349', '11361', '11362', '11363', '11365', '11369', '11381', '11383', '11385', '11408', '11442', '11464', '11465'],
    ['12101', '12102', '12103', '12104', '12105', '12106', '12202', '12203', '12204', '12205', '12206', '12207', '12208', '12210', '12211', '12212', '12213', '12215', '12216', '12217', '12218', '12219', '12220', '12221', '12222', '12223', '12224', '12225', '12226', '12227', '12228', '12229', '12230', '12231', '12232', '12233', '12234', '12235', '12236', '12237', '12238', '12239', '12322', '12329', '12342', '12347', '12349', '12403', '12409', '12410', '12421', '12422', '12423', '12424', '12426', '12427', '12441', '12443', '12463'],
    ['13101', '13102', '13103', '13104', '13105', '13106', '13107', '13108', '13109', '13110', '13111', '13112', '13113', '13114', '13115', '13116', '13117', '13118', '13119', '13120', '13121', '13122', '13123', '13201', '13202', '13203', '13204', '13205', '13206', '13207', '13208', '13209', '13210', '13211', '13212', '13213', '13214', '13215', '13218', '13219', '13220', '13221', '13222', '13223', '13224', '13225', '13227', '13228', '13229', '13303', '13305', '13307', '13308', '13361', '13362', '13363', '13364', '13381', '13382', '13401', '13402', '13421'],
    ['14131', '14132', '14133', '14134', '14135', '14136', '14137', '14101', '14102', '14103', '14104', '14105', '14106', '14107', '14108', '14109', '14110', '14111', '14112', '14113', '14114', '14115', '14116', '14117', '14118', '14151', '14152', '14153', '14201', '14203', '14204', '14205', '14206', '14207', '14208', '14210', '14211', '14212', '14213', '14214', '14215', '14216', '14217', '14218', '14301', '14321', '14341', '14342', '14361', '14362', '14363', '14364', '14366', '14382', '14383', '14384', '14401', '14402'],
    ['15101', '15102', '15103', '15104', '15105', '15106', '15107', '15108', '15202', '15204', '15205', '15206', '15208', '15209', '15210', '15211', '15212', '15213', '15216', '15217', '15218', '15222', '15223', '15224', '15225', '15226', '15227', '15307', '15342', '15361', '15385', '15405', '15461', '15482', '15504', '15581', '15586'],
    ['16201', '16202', '16204', '16205', '16206', '16207', '16208', '16209', '16210', '16211', '16321', '16322', '16323', '16342', '16343'],
    ['17201', '17202', '17203', '17204', '17205', '17206', '17207', '17209', '17210', '17211', '17212', '17324', '17361', '17365', '17384', '17386', '17407', '17461', '17463'],
    ['18201', '18202', '18204', '18205', '18206', '18207', '18208', '18209', '18210', '18322', '18382', '18404', '18423', '18442', '18481', '18483', '18501'],
    ['19201', '19202', '19204', '19205', '19206', '19207', '19208', '19209', '19210', '19211', '19212', '19213', '19214', '19346', '19364', '19365', '19366', '19368', '19384', '19422', '19423', '19424', '19425', '19429', '19430', '19442', '19443'],
    ['20201', '20202', '20203', '20204', '20205', '20206', '20207', '20208', '20209', '20210', '20211', '20212', '20213', '20214', '20215', '20217', '20218', '20219', '20220', '20303', '20304', '20305', '20306', '20307', '20309', '20321', '20323', '20324', '20349', '20350', '20361', '20362', '20363', '20382', '20383', '20384', '20385', '20386', '20388', '20402', '20403', '20404', '20407', '20409', '20410', '20411', '20412', '20413', '20414', '20415', '20416', '20417', '20422', '20423', '20425', '20429', '20430', '20432', '20446', '20448', '20450', '20451', '20452', '20481', '20482', '20485', '20486', '20521', '20541', '20543', '20561', '20562', '20563', '20583', '20588', '20590', '20602'],
    ['21201', '21202', '21203', '21204', '21205', '21206', '21207', '21208', '21209', '21210', '21211', '21212', '21213', '21214', '21215', '21216', '21217', '21218', '21219', '21220', '21221', '21302', '21303', '21341', '21361', '21362', '21381', '21382', '21383', '21401', '21403', '21404', '21421', '21501', '21502', '21503', '21504', '21505', '21506', '21507', '21521', '21604'],
    ['22101', '22102', '22103', '22131', '22132', '22133', '22134', '22135', '22136', '22137', '22203', '22205', '22206', '22207', '22208', '22209', '22210', '22211', '22212', '22213', '22214', '22215', '22216', '22219', '22220', '22221', '22222', '22223', '22224', '22225', '22226', '22301', '22302', '22304', '22305', '22306', '22325', '22341', '22342', '22344', '22424', '22429', '22461'],
    ['23101', '23102', '23103', '23104', '23105', '23106', '23107', '23108', '23109', '23110', '23111', '23112', '23113', '23114', '23115', '23116', '23201', '23202', '23203', '23204', '23205', '23206', '23207', '23208', '23209', '23210', '23211', '23212', '23213', '23214', '23215', '23216', '23217', '23219', '23220', '23221', '23222', '23223', '23224', '23225', '23226', '23227', '23228', '23229', '23230', '23231', '23232', '23233', '23234', '23235', '23236', '23237', '23238', '23302', '23342', '23361', '23362', '23424', '23425', '23427', '23441', '23442', '23445', '23446', '23447', '23501', '23561', '23562', '23563'],
    ['24201', '24202', '24203', '24204', '24205', '24207', '24208', '24209', '24210', '24211', '24212', '24214', '24215', '24216', '24303', '24324', '24341', '24343', '24344', '24441', '24442', '24443', '24461', '24470', '24471', '24472', '24543', '24561', '24562'],
    ['25201', '25202', '25203', '25204', '25206', '25207', '25208', '25209', '25210', '25211', '25212', '25213', '25214', '25383', '25384', '25425', '25441', '25442', '25443'],
    ['26101', '26102', '26103', '26104', '26105', '26106', '26107', '26108', '26109', '26110', '26111', '26201', '26202', '26203', '26204', '26205', '26206', '26207', '26208', '26209', '26210', '26211', '26212', '26213', '26214', '26303', '26322', '26343', '26344', '26364', '26365', '26366', '26367', '26407', '26463', '26465'],
    ['27102', '27103', '27104', '27106', '27107', '27108', '27109', '27111', '27113', '27114', '27115', '27116', '27117', '27118', '27119', '27120', '27121', '27122', '27123', '27124', '27125', '27126', '27127', '27128', '27141', '27142', '27143', '27144', '27145', '27146', '27147', '27202', '27203', '27204', '27205', '27206', '27207', '27208', '27209', '27210', '27211', '27212', '27213', '27214', '27215', '27216', '27217', '27218', '27219', '27220', '27221', '27222', '27223', '27224', '27225', '27226', '27227', '27228', '27229', '27230', '27231', '27232', '27301', '27321', '27322', '27341', '27361', '27362', '27366', '27381', '27382', '27383'],
    ['28101', '28102', '28105', '28106', '28107', '28108', '28109', '28110', '28111', '28201', '28202', '28203', '28204', '28205', '28206', '28207', '28208', '28209', '28210', '28212', '28213', '28214', '28215', '28216', '28217', '28218', '28219', '28220', '28221', '28222', '28223', '28224', '28225', '28226', '28227', '28228', '28229', '28301', '28365', '28381', '28382', '28442', '28443', '28446', '28464', '28481', '28501', '28585', '28586'],
    ['29201', '29202', '29203', '29204', '29205', '29206', '29207', '29208', '29209', '29210', '29211', '29212', '29322', '29342', '29343', '29344', '29345', '29361', '29362', '29363', '29385', '29386', '29401', '29402', '29424', '29425', '29426', '29427', '29441', '29442', '29443', '29444', '29446', '29447', '29449', '29450', '29451', '29452', '29453'],
    ['30201', '30202', '30203', '30204', '30205', '30206', '30207', '30208', '30209', '30304', '30341', '30343', '30344', '30361', '30362', '30366', '30381', '30382', '30383', '30390', '30391', '30392', '30401', '30404', '30406', '30421', '30422', '30424', '30427', '30428'],
    ['31201', '31202', '31203', '31204', '31302', '31325', '31328', '31329', '31364', '31370', '31371', '31372', '31384', '31386', '31389', '31390', '31401', '31402', '31403'],
    ['32201', '32202', '32203', '32204', '32205', '32206', '32207', '32209', '32343', '32386', '32441', '32448', '32449', '32501', '32505', '32525', '32526', '32527', '32528'],
    ['33101', '33102', '33103', '33104', '33202', '33203', '33204', '33205', '33207', '33208', '33209', '33210', '33211', '33212', '33213', '33214', '33215', '33216', '33346', '33423', '33445', '33461', '33586', '33606', '33622', '33623', '33643', '33663', '33666', '33681'],
    ['34101', '34102', '34103', '34104', '34105', '34106', '34107', '34108', '34202', '34203', '34204', '34205', '34207', '34208', '34209', '34210', '34211', '34212', '34213', '34214', '34215', '34302', '34304', '34307', '34309', '34368', '34369', '34431', '34462', '34545'],
    ['35201', '35202', '35203', '35204', '35206', '35207', '35208', '35210', '35211', '35212', '35213', '35215', '35216', '35305', '35321', '35341', '35343', '35344', '35502'],
    ['36201', '36202', '36203', '36204', '36205', '36206', '36207', '36208', '36301', '36302', '36321', '36341', '36342', '36368', '36383', '36387', '36388', '36401', '36402', '36403', '36404', '36405', '36468', '36489'],
    ['37201', '37202', '37203', '37204', '37205', '37206', '37207', '37208', '37322', '37324', '37341', '37364', '37386', '37387', '37403', '37404', '37406'],
    ['38201', '38202', '38203', '38204', '38205', '38206', '38207', '38210', '38213', '38214', '38215', '38356', '38386', '38401', '38402', '38422', '38442', '38484', '38488', '38506'],
    ['39201', '39202', '39203', '39204', '39205', '39206', '39208', '39209', '39210', '39211', '39212', '39301', '39302', '39303', '39304', '39305', '39306', '39307', '39341', '39344', '39363', '39364', '39386', '39387', '39401', '39402', '39403', '39405', '39410', '39411', '39412', '39424', '39427', '39428'],
    ['40131', '40132', '40133', '40134', '40135', '40136', '40137', '40101', '40103', '40105', '40106', '40107', '40108', '40109', '40202', '40203', '40204', '40205', '40206', '40207', '40210', '40211', '40212', '40213', '40214', '40215', '40216', '40217', '40218', '40219', '40220', '40221', '40223', '40224', '40225', '40226', '40227', '40228', '40229', '40230', '40231', '40341', '40342', '40343', '40344', '40345', '40348', '40349', '40381', '40382', '40383', '40384', '40401', '40402', '40421', '40447', '40448', '40503', '40522', '40544', '40601', '40602', '40604', '40605', '40608', '40609', '40610', '40621', '40625', '40642', '40646', '40647'],
    ['41201', '41202', '41203', '41204', '41205', '41206', '41207', '41208', '41209', '41210', '41327', '41341', '41345', '41346', '41387', '41401', '41423', '41424', '41425', '41441'],
    ['42201', '42202', '42203', '42204', '42205', '42207', '42208', '42209', '42210', '42211', '42212', '42213', '42214', '42307', '42308', '42321', '42322', '42323', '42383', '42391', '42411'],
    ['43101', '43102', '43103', '43104', '43105', '43202', '43203', '43204', '43205', '43206', '43208', '43210', '43211', '43212', '43213', '43214', '43215', '43216', '43348', '43364', '43367', '43368', '43369', '43403', '43404', '43423', '43424', '43425', '43428', '43432', '43433', '43441', '43442', '43443', '43444', '43447', '43468', '43482', '43484', '43501', '43505', '43506', '43507', '43510', '43511', '43512', '43513', '43514', '43531'],
    ['44201', '44202', '44203', '44204', '44205', '44206', '44207', '44208', '44209', '44210', '44211', '44212', '44213', '44214', '44322', '44341', '44461', '44462'],
    ['45201', '45202', '45203', '45204', '45205', '45206', '45207', '45208', '45209', '45341', '45361', '45382', '45383', '45401', '45402', '45403', '45404', '45405', '45406', '45421', '45429', '45430', '45431', '45441', '45442', '45443'],
    ['46201', '46203', '46204', '46206', '46208', '46210', '46213', '46214', '46215', '46216', '46217', '46218', '46219', '46220', '46221', '46222', '46223', '46224', '46225', '46303', '46304', '46392', '46404', '46452', '46468', '46482', '46490', '46491', '46492', '46501', '46502', '46505', '46523', '46524', '46525', '46527', '46529', '46530', '46531', '46532', '46533', '46534', '46535'],
    ['47201', '47205', '47207', '47208', '47209', '47210', '47211', '47212', '47213', '47214', '47215', '47301', '47302', '47303', '47306', '47308', '47311', '47313', '47314', '47315', '47324', '47325', '47326', '47327', '47328', '47329', '47348', '47350', '47353', '47354', '47355', '47356', '47357', '47358', '47359', '47360', '47361', '47362', '47375', '47381', '47382']
]

ken_list = ['01', '01', '02', '02', '03', '03', '04', '04', '05', '05', '06', '06', '07', '07', '08', '08', '09', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47']

kenmei_list = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

data = {'toriatu_parking_fl': '1',
            'sort': '102',
            'syougo': None,
            'display_count': '100',
            'page': 1}

kaiin_code_list = []

headers = [
    '商号', '住所', '電話', '代表者', '免許番号', '主な取り扱い物件','交通'
]


def corporate_code_parser(start):
    i = start
    ken = ken_list[i - 1]
    list_number = 0
    kenwake_code_list = []
    syogo_list = []
    amount = len(siku_code[i-1])
    bar = tqdm.tqdm(total=amount)
    bar.set_description(f'{kenmei_list[i-1]}の会社コード取得進行状況')
    while True:
        try:
            post_code = siku_code[i-1][list_number]
            res = requests.post(
                f'https://www.hatomarksite.com/search/zentaku/agent/area/?pref={ken}&syz={post_code}', data=data)
            # print(res.status_code)
            json = res.json()
            try:
                if json['agent']:
                    agent = json['agent']
            except:
                bar.update(1)
                list_number += 1
                time.sleep(2)
                continue
            agent_roop_number = 0
            time.sleep(1)
            while True:
                try:
                    kaiin_number = agent[agent_roop_number]['kai_no']
                    syogo = agent[agent_roop_number]['syougo']
                    kenwake_code_list.append(kaiin_number)
                    syogo_list.append(syogo)
                    agent_roop_number += 1
                except:
                    bar.update(1)
                    list_number += 1
                    break
        except:
            with open(f'hatosite/code/{kenmei_list[i-1]}' + '.csv', 'w' ) as w:
                row = ['商号', '会員番号']
                writer = csv.writer(w)
                writer.writerow(row)
                len_number = len(kenwake_code_list)
                for i in range(0, len_number):
                    writer.writerow([syogo_list[i], kenwake_code_list[i]])
            break


def corporate_code_parser_kai(start):
    i = start
    ken = ken_list[i - 1]
    list_number = 0
    kenwake_code_list = []
    syogo_list = []
    code_list = []
    amount = len(siku_code[i-1])
    post_code = siku_code[i-1]
    len_post_code = len(post_code)
    amari = len_post_code % 5
    syou = len_post_code // 5
    for l in range(0, syou):
        joined_list_number = post_code[l*5:(l+1)*5]
        joined_number = ''
        for k in joined_list_number:
            if joined_number == '':
                joined_number = k
            else:
                joined_number = joined_number+ '|' + k
        code_list.append(joined_number)
    m = post_code[syou*5:syou*5+amari]
    joined_number = ''
    for k in m:
        if joined_number == '':
            joined_number = k
        else:
            joined_number = joined_number + '|' + k
    code_list.append(joined_number)
    for code in code_list:
        print(code)
        res = requests.post(
            f'https://www.hatomarksite.com/search/zentaku/agent/area/?pref={ken}&syz={code}', data=data)
        # print(res.status_code)
        json = res.json()
        try:
            if json['agent']:
                agent = json['agent']
        except:
            list_number += 1
            time.sleep(2)
            continue
        agent_roop_number = 0
        while True:
            try:
                kaiin_number = agent[agent_roop_number]['kai_no']
                syogo = agent[agent_roop_number]['syougo']
                kenwake_code_list.append(kaiin_number)
                syogo_list.append(syogo)
                agent_roop_number += 1
            except:
                list_number += 1
                time.sleep(1)
                break
    with open(f'hatosite/code/{kenmei_list[i-1]}' + '.csv', 'w' ) as w:
        row = ['商号', '会員番号']
        writer = csv.writer(w)
        writer.writerow(row)
        len_number = len(kenwake_code_list)
        for i in range(0, len_number):
            writer.writerow([syogo_list[i], kenwake_code_list[i]])



def shop_parser(kenwake_code_list, list_number):
    csv_data = []
    parserd_data_list = []
    amount = len(kenwake_code_list)
    bar = tqdm.tqdm(total=amount)
    bar.set_description(f'{kenmei_list[list_number - 1]}のスクレイピング進行状況')
    for number in kenwake_code_list:
        res = requests.get(
            f'https://www.hatomarksite.com/search/zentaku/agent/{number}')
        soup = bs4.BeautifulSoup(res.content, "html.parser")
        data_list = soup.find_all('td')
        for i in data_list:
            parserd_data_list.append(i.get_text())
        try:
            syogo = parserd_data_list[0]
            address = parserd_data_list[1]
            phone_number = parserd_data_list[2]
            koutuu = parserd_data_list[3]
            representer = parserd_data_list[6]
            menkyo = parserd_data_list[8]
            bukken = parserd_data_list[9]
        except:
            continue
            bar.update(1)
        row = [syogo, address, phone_number, representer, menkyo, bukken, koutuu]
        csv_data.append(row)
        bar.update(1)
        print('\n')
        print(row)
        parserd_data_list = []
        time.sleep(2)
    with open('hatosite/' + kenmei_list[list_number-1] + '.csv', 'w') as w:
        writer = csv.writer(w)
        writer.writerows([headers])
        writer.writerows(csv_data)


def shop_parserkai(ken_number, data_length=100):
    csv_data = []
    parserd_data_list = []
    with open(f'hatosite/code/{kenmei_list[ken_number-1]}' + '.csv', 'r') as r:
        reader = csv.reader(r)
        next(reader)
        counter = 0
        data_length = data_length
        for row in reader:
            if data_length == counter:
                break
            number = row[1]
            res = requests.get(
                f'https://www.hatomarksite.com/search/zentaku/agent/{number}')
            soup = bs4.BeautifulSoup(res.content, "html.parser")
            data_list = soup.find_all('td')
            for i in data_list:
                parserd_data_list.append(i.get_text())
            try:
                syogo = parserd_data_list[0]
                address = parserd_data_list[1]
                phone_number = parserd_data_list[2]
                koutuu = parserd_data_list[3]
                representer = parserd_data_list[6]
                menkyo = parserd_data_list[8]
                bukken = parserd_data_list[9]
            except:
                continue
            row = [syogo, address, phone_number, representer, menkyo, bukken, koutuu]
            csv_data.append(row)
            print(row)
            df = pd.read_csv(f'hatosite/code/{kenmei_list[ken_number - 1]}' + '.csv', dtype=object)
            droped_df = df.drop([0])
            droped_df.to_csv(f'hatosite/code/{kenmei_list[ken_number - 1]}' + '.csv', index=False)
            parserd_data_list = []
            counter += 1
            time.sleep(2)
    number = ''
    while True:
        str_number = str(number)
        if not os.path.exists('hatosite/' + kenmei_list[ken_number - 1] + str_number + '.csv'):
            with open('hatosite/' + kenmei_list[ken_number - 1] + str_number + '.csv', 'w') as w:
                writer = csv.writer(w)
                writer.writerows([headers])
                writer.writerows(csv_data)
            break
        else:
            if number == '':
                number = 1
            number += 1
            continue
    print(f'{kenmei_list[ken_number - 1]}のCSVファイルを出力しました。')


def sikucode_parser():
    with open('hatsite.html', encoding='utf-8') as f:
        html = f.read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    j = soup.find_all('input')
    siku_code1 = []
    for i in j:
        siku_code1.append(i.get('value'))
    print(siku_code1)


if __name__ == '__main__':
    # shop_parserkai(1,data_length=5)
    # res = requests.post(
    #     f'https://www.hatomarksite.com/search/zentaku/agent/area/?pref=01&syz=01101', data=data)
    # # print(res.status_code)
    # json = res.json()
    # pprint(json)
    lists = []
    for i in range(1, 48):
        try:
            with open(f'hatosite/code/{kenmei_list[i - 1]}' + '.csv', 'r') as r:
                reader = csv.reader(r)
                next(reader)
                lens = len([row for row in reader])
                k = [kenmei_list[i - 1], lens]
                lists.append(k)
        except:
            continue
    with open('情報2.csv', 'w') as w:
        writer = csv.writer(w)
        writer.writerows(lists)