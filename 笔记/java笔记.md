
java：
URLEncoder.encode("计划");//url编码
    Random random = new Random();
    random.nextInt()
    int baseIndex = (int)(Math.random());
    throw new Exception("参数不能为空!")//抛出异常
    byte[] gbkN = string.getBytes("GBK");//得到

注意：headers最好要加上，否则可能请求不出来（返回200，但没有数据）Content-Type：


时间：SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");



class yingyongbao implements CollectCoreScript{}
static {header.put("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");};
@SeedProcessor
    Request processParameter(String param) {}
    Request request = new Request(url, HttpRequestMethod.get, parameter, headers);
    request.addHeader("","");
    Map<String, String> paramMap = new HashMap<String, String>();
    paramMap.put("","")
    request.setUrlContext(paramMap);
    request.useUrlContextDedup = true;//urlContext去重

@Override
    Result parse(Page page) {}
    Result result = new Result();
    Html html = page.html;
    page.getPageEncode()
    page.setPageEncode("UTF-8");
    page.statusCode
    String url = page.request.url;
    page.request.getHeaders().get("Cookie")
    String apkName = page.getRequest().getUrlContext().get("apkName");

    Parameter p = new Parameter();
    p.setFormParameters(paramMap);
    p.setTextParameter("{}");//设置text类型参数

    result.addChildLink(request);
    result.addDataMap(dataMap);

Html:
    Selectable container = html.$(".det-ins-container");
    List<Selectable> liList=html.$('.mod-result').xpath("/ul/li").nodes()
    String appDownload = html.$(".det-insnum-line").xpath("/div/div[1]/text()").get()
    xpath("/div/div[1]/allText()").get()


Map:
    Map<String,String> map = page.request.urlContext;
    String level = map.get("level");
    map.put("","");
    map.allPut(map对象);
    private static List<String> cookieList = new ArrayList<String>();//list
    cookieList.add()
    cookieList.size()
    cookieList.remove()


Json:
    JSONObject jsonObject = JSONObject.parse(rawPage);
    JSONArray dataArray = jsonObject.getJSONArray("root")
    jsonObject.get("msg")
    JSONObject.toJSONString(some)


String:
    string.equals("请求失败")//返回true或false类似==（有不同）
    string.contains("")//包含
    StringUtils.trim()//去左右空格
    string.split("")//分割
    int data1 = totalUrl.indexOf("z0b0r0c0x0y0t0m0q0s0p");//得到查找内容在字符串中的位置
    String data3 = totalUrl.substring(0,data1);//根据位置返回字符串中的内容
    string转换:
    int data4 = Integer.parseInt(data3);
    int data4 = Integer.valueOf（data3）;
    String data8 = Integer.toString(data4);
    String data11 =	String.valueOf（data7）;
    String data12 = ""+data4+data5+data6+data7;
    new String(byte[], decode)

正则：
    String pattern = "[\\s\\S]*?上传";
    String replaceData = "";
    Pattern r = Pattern.compile(pattern);//patter类
    Matcher m = r.matcher(data); //matcher类
    data = m.replaceFirst(replaceData);



for:
    for (JSONObject dataObject : dataArray){}
    for (int i = 0; i <= numberPage; i++) {}//循环结束后才进行i++

列表：   List<String> listKeyWord = new ArrayList<>();
        listKeyWord.add(keyword1);