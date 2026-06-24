#!/usr/bin/env python3
"""Generate SpeedCE CSDN article library."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "articles" / "csdn"
OUT.mkdir(parents=True, exist_ok=True)

HEADER = """> 工具地址：https://www.speedce.com  
> 中文界面：https://speedce.com/?lang=zh-CN  
> 联系：speedceads@gmail.com

---

"""

FOOTER = """
---

**关键词**：{keywords}

"""

# (slug, title, category, intro, scenarios, focus_nodes, protocol, keywords)
ARTICLES = [
    # === 已有手工精品（跳过生成）===
    # vps-line-verification-guide, cdn-deployment, global-deployment

    # === A. 故障排查系列 01-20 ===
    ("dns-troubleshooting-guide", "DNS 解析故障完全指南：迁机、换 CDN 后「部分地区打不开」怎么查", "故障排查",
     "DNS 问题是「我这边正常、他那边不行」的头号元凶。TTL、缓存、分线路解析、污染——都需要用多节点视角验证。",
     ["迁机后同事仍访问旧 IP", "仅某一省份解析错误", "子域解析到错误 CNAME", "全球与中国的解析结果不一致"],
     "中国节点", "HTTPS", "DNS故障排查,多节点测速,SpeedCE,域名解析,迁机"),

    ("ssl-certificate-troubleshooting", "SSL 证书过期与配置错误：用户报「连接不安全」时怎么 10 分钟定位", "故障排查",
     "证书问题常表现为：你本地能开（HSTS/缓存），用户大面积报错。多节点 HTTPS 测速是第一现场。",
     ["Let's Encrypt 续签失败", "SAN 漏配 api 子域", "海外节点证书不信任", "HTTP 正常 HTTPS 全红"],
     "中国节点+全球节点", "HTTPS", "SSL证书,HTTPS测速,证书过期,SpeedCE"),

    ("nginx-reverse-proxy-troubleshooting", "Nginx 反向代理配置故障排查：主站绿、API 红的典型原因", "故障排查",
     "Nginx 的 server_name、proxy_pass、证书、upstream——任何一环错，地图就会红。",
     ["只配了 www 没配根域", "API 子域证书漏签", "回源 Host 错误导致 404", "502 上游超时"],
     "中国节点", "HTTPS", "Nginx,反向代理,网站故障,SpeedCE"),

    ("website-migration-guide", "网站迁机完整手册：DNS、源站、CDN 切换的测速验收节奏", "故障排查",
     "迁机不是改完 DNS 就结束。72 小时内的多节点点检，决定用户投诉量。",
     ["全国 sporadic 红逐渐变绿", "固定省份持续红", "迁机后全国全红", "新旧 IP 对照"],
     "中国节点", "HTTPS", "网站迁机,DNS切换,多节点测速,SpeedCE"),

    ("intermittent-fault-diagnosis", "间歇性网站故障怎么查：「有时慢有时好」的点检方法", "故障排查",
     "间歇故障最难搞——你测的时候刚好正常。固定间隔多次测速，看通畅率曲线。",
     ["晚高峰才红", "随机 sporadic 异常", "固定省份间歇红", "攻击导致间歇不可用"],
     "中国节点", "HTTPS", "间歇性故障,网站不稳定,多节点测速,SpeedCE"),

    ("subdomain-troubleshooting", "子域名故障排查完全指南：主站能开、接口挂了的 6 种原因", "故障排查",
     "www 和 api、cdn、m 往往独立配置。每个对外子域都该有一张地图。",
     ["api 子域证书问题", "CDN 只加速 www", "CNAME 链错误", "子域未备案被拦"],
     "中国节点", "HTTPS", "子域名,DNS,API故障,SpeedCE"),

    ("api-availability-guide", "API 接口可达性检测指南：Postman 能通、用户不通的真相", "故障排查",
     "开发本地通、全国不通——多半是 DNS、证书、防火墙或 Geo 限制。",
     ["移动端 API 失败", "仅 POST 失败（测速测 GET 可达性）", "海外调用国内 API", "跨域与网络层分工"],
     "中国节点+全球节点", "HTTPS", "API监控,接口测速,SpeedCE,后端"),

    ("http-https-redirect-issues", "HTTP 与 HTTPS 跳转问题排查：强制跳转、混合内容、循环重定向", "故障排查",
     "跳转配错会导致部分节点超时或证书错误。HTTP 与 HTTPS 模式对照测。",
     ["301 循环", "仅 HTTP 可访问", "部分省份 HTTPS 红", "HSTS 导致旧证书残留"],
     "中国节点", "HTTP+HTTPS", "HTTPS跳转,SSL,网站配置,SpeedCE"),

    ("firewall-security-group-checklist", "云服务器安全组与防火墙验收：全国红的第一排查项", "故障排查",
     "全国地图大面积红，先别怪线路——80/443/ICMP 放行了吗？",
     ["只放了 22 没放 443", "CDN 回源 IP 未白名单", "iptables 误拦", "云厂商默认拒绝"],
     "中国节点", "HTTPS+PING", "安全组,防火墙,云服务器,SpeedCE"),

    ("502-503-upstream-errors", "502/503 错误与源站过载：CDN 绿、源站红的判断法", "故障排查",
     "边缘节点能连上，回源失败——用户看到 502。对照测 CDN 域名与源站 IP。",
     ["大促流量打满", "PHP-FPM 池耗尽", "回源超时设置过短", "单点源站宕机"],
     "中国节点", "HTTPS", "502错误,源站过载,CDN回源,SpeedCE"),

    ("dns-propagation-slow", "域名解析生效慢怎么判断：TTL、缓存与区域 DNS 差异", "故障排查",
     "改完 DNS 不是全世界立刻生效。多节点、多次测，看异常点是否随时间减少。",
     ["TTL 86400 导致慢", "某省运营商缓存顽固", "本地 hosts 误导排查", "分线路解析未生效"],
     "中国节点", "HTTPS", "DNS缓存,TTL,域名生效,SpeedCE"),

    ("regional-access-failure", "仅部分地区打不开？用地图精确定位省份与运营商", "故障排查",
     "「就新疆不行」「就移动不行」——三网分离 + 地图比平均延迟有用一万倍。",
     ["单省全红", "西北片区红", "华南绿华北红", "边境省份异常"],
     "中国节点", "HTTPS", "部分地区打不开,区域故障,三网测速,SpeedCE"),

    ("mobile-network-issues", "移动网络用户访问异常专项指南：为什么移动投诉最多", "故障排查",
     "移动用户占比超 50%，但很多线路只优化电信联通。移动地图必须单独看。",
     ["电信绿移动红", "移动 4G/5G 差异", "移动 DNS 污染", "移动国际出口慢"],
     "中国节点+移动筛选", "HTTPS", "移动网络,三网测速,SpeedCE,运营商"),

    ("single-carrier-fault", "电信/联通/移动单网故障排查：一张网全红的处理流程", "故障排查",
     "三网分离后只有一张网红——问题范围立刻缩小一半。",
     ["仅电信红", "仅联通红", "仅移动红", "教育网用户反馈"],
     "中国节点", "HTTPS", "电信,联通,移动,单网故障,SpeedCE"),

    ("peak-hour-slowdown", "晚高峰网站变慢排查：下午绿、晚上红的复测方法", "故障排查",
     "带宽、线路拥堵、攻击——晚高峰才是照妖镜。固定 20:00–22:00 复测。",
     ["跨省带宽打满", "国际线路晚高峰堵", "CC 攻击", "源站 CPU 飙升"],
     "中国节点", "HTTPS", "晚高峰,网站变慢,线路拥堵,SpeedCE"),

    ("ddos-attack-detection", "被攻击时如何用多节点测速辅助判断", "故障排查",
     "测速不能替代 DDoS 防护，但全国同时变红 + 源站告警，可快速确认攻击面。",
     ["全国延迟飙升", "间歇性全国红", "仅 80 端口异常", "攻击结束后的恢复验证"],
     "中国节点", "HTTPS", "DDoS,网站攻击,故障排查,SpeedCE"),

    ("ipv6-troubleshooting", "IPv6 访问异常排查：双栈站点的验收与对照", "故障排查",
     "IPv4 全绿不代表 IPv6 正常。SpeedCE 支持 IPv6 目标，双栈各测一遍。",
     ["AAAA 记录配错", "IPv6 防火墙未放行", "仅 IPv6 用户反馈", "CDN 未开 IPv6"],
     "中国节点+全球节点", "HTTPS", "IPv6,双栈,网站验收,SpeedCE"),

    ("mixed-content-https", "混合内容与 HTTPS 报错：网络层绿、浏览器仍报不安全", "故障排查",
     "SpeedCE 测的是站点可达性，混合内容是页面层——分工要明确。",
     ["资源 HTTP 引用", "第三方脚本非 HTTPS", "CDN 回源 HTTP", "修复后复测 HTTPS"],
     "中国节点", "HTTPS", "混合内容,HTTPS,前端安全,SpeedCE"),

    ("cors-vs-network-testing", "CORS 报错 vs 网络不通：开发者分清两层问题", "故障排查",
     "地图全绿但前端报 CORS——说明网络通了，是应用配置问题。",
     ["浏览器报 CORS", "App 能开网页不行", "预检 OPTIONS 失败", "跨域与测速分工"],
     "中国节点", "HTTPS", "CORS,跨域,API,SpeedCE"),

    ("wechat-qq-access-guide", "微信/QQ 打不开先测什么：网络层与合规层分工指南", "故障排查",
     "SpeedCE 排除网络层；拦截/备案/内容合规用专项工具。先测再猜。",
     ["浏览器正常微信不行", "全国绿仍被拦", "备案问题", "域名被标记"],
     "中国节点", "HTTPS", "微信拦截,QQ打不开,网站合规,SpeedCE"),

    # === B. VPS与线路 21-35 ===
    ("hong-kong-vps-guide", "香港 VPS 线路选购与验收：个人站、电商、API 怎么选", "VPS线路",
     "香港是国人最熟悉的机房。CN2、CMI、BGP 混杂，地图验收是必修课。",
     ["香港 CN2 验收", "移动用户访问香港", "香港到全球延迟", "香港 IP 被墙风险"],
     "中国节点+全球节点", "HTTPS+PING", "香港VPS,CN2,线路测速,SpeedCE"),

    ("japan-vps-guide", "日本 VPS 适合什么业务：延迟、带宽与三网回国实测", "VPS线路",
     "日本机房便宜、带宽足，但回国线路参差不齐。付款前必测三网。",
     ["东京 vs 大阪", "日本到美国延迟", "三网回国质量", "晚高峰复测"],
     "中国节点", "PING+HTTPS", "日本VPS,线路测评,SpeedCE"),

    ("us-vps-china-access", "美国 VPS 三网回国测评方法：西海岸机房怎么验", "VPS线路",
     "美国机便宜大碗，移动用户可能是灾难。看地图再下单。",
     ["洛杉矶线路", "圣何塞 CN2", "美国到欧洲", "被墙检测配合"],
     "中国节点+全球节点", "PING+HTTPS", "美国VPS,三网测速,回国线路,SpeedCE"),

    ("singapore-vps-guide", "新加坡 VPS 验收指南：东南亚与回国双视角", "VPS线路",
     "新加坡是出海亚太枢纽，也是回国中继。双视图测速一次搞定。",
     ["新加坡回国", "新加坡到印尼马来", "BGP 验收", "带宽峰值"],
     "中国节点+全球节点", "HTTPS", "新加坡VPS,东南亚,SpeedCE"),

    ("cn2-gt-vs-gia", "CN2 GT 与 CN2 GIA 怎么选：商家话术背后的测速验证", "VPS线路",
     "名字差两个字母，体验差一个档次。用三网地图验证，别信文案。",
     ["GT 晚高峰", "GIA 移动表现", "价格与质量平衡", "论坛对照 IP"],
     "中国节点", "PING+HTTPS", "CN2 GT,CN2 GIA,VPS选购,SpeedCE"),

    ("bgp-line-verification", "BGP 线路真假辨别：三网均衡才是真的 BGP", "VPS线路",
     "假 BGP：电信绿、移动红。真 BGP：三网都能看。",
     ["三网延迟对比", "非 BGP 绕路", "BGP 晚高峰", "同价竞品对照"],
     "中国节点", "PING", "BGP线路,VPS,三网测速,SpeedCE"),

    ("cmi-mobile-line-guide", "移动优化（CMI）线路验收标准：移动用户站必看", "VPS线路",
     "移动占比过半的时代，移动地图一票否决权。",
     ["CMI 标识验证", "移动西北表现", "与电信联通对比", "移动 5G 用户"],
     "中国节点+移动", "HTTPS", "CMI,移动线路,VPS,SpeedCE"),

    ("vps-refund-period-checklist", "VPS 7 天退款期验机清单：不满意就退的证据链", "VPS线路",
     "截图 + 三网数据 + 晚高峰复测 = 退款成功率翻倍。",
     ["到账 IP 对照", "测试 IP 缩水", "带宽虚标", "丢包与延迟"],
     "中国节点", "HTTPS+PING", "VPS退款,验机,SpeedCE"),

    ("cloud-security-group-vps", "云服务器安全组验收：验机第一步不是 Ping 是端口", "VPS线路",
     "新机到手全国红？先开 443 再谈线路。",
     ["阿里云安全组", "腾讯云防火墙", "轻量云默认规则", "ICMP 与 Web"],
     "中国节点", "HTTPS+PING", "安全组,VPS,云服务器,SpeedCE"),

    ("ping-blocked-not-bad", "禁 Ping 不等于线路差：PING 红 HTTPS 绿怎么解读", "VPS线路",
     "新手最怕 Ping 超时。学会切换 HTTPS 模式救心态。",
     ["云厂商禁 ICMP", "安全组拦 Ping", "HTTPS 验收标准", "勿误退好机器"],
     "中国节点", "PING+HTTPS", "禁Ping,VPS,ICMP,SpeedCE"),

    ("off-peak-vs-peak-vps", "VPS 下午测与晚高峰测：为什么必须测两次", "VPS线路",
     "商家挑下午给你看测试 IP。你要在晚高峰复测。",
     ["20:00 复测", "通畅率波动", "丢包对比", "退款依据"],
     "中国节点", "PING+HTTPS", "晚高峰,VPS测速,线路,SpeedCE"),

    ("home-broadband-vs-datacenter", "家宽与机房测速差异：为什么你 Ping 快全国慢", "VPS线路",
     "你在同城家宽测 VPS，延迟天然虚低。全国节点才是用户视角。",
     ["同城偏见", "家宽运营商", "机房测速误导", "正确验收姿势"],
     "中国节点", "HTTPS", "测速方法,VPS,偏见,SpeedCE"),

    ("vps-with-cdn-comparison", "VPS 套 CDN 前后对比测速：该不该上 CDN 的数据依据", "VPS线路",
     "源站地图与 CDN 地图并排，加速有没有用一目了然。",
     ["源站绿 CDN 红", "移动改善明显", "全球改善", "回源带宽"],
     "中国节点", "HTTPS", "VPS,CDN,对比测速,SpeedCE"),

    ("used-ip-segment-check", "二手 IP 段怎么验：被墙、被标记的 IP 购买前避雷", "VPS线路",
     "便宜 IP 可能有前科。中国全红、全球绿——警惕被墙。",
     ["全球绿中国红", "邮件发不出", "SEO 受影响", "换 IP 复测"],
     "中国节点+全球节点", "HTTPS+PING", "IP被墙,VPS,二手IP,SpeedCE"),

    ("datacenter-failover-verify", "机房故障换机后如何快速验证：应急测速 SOP", "VPS线路",
     "故障迁移后，全国点检确认新业务 IP 是否正常。",
     ["紧急切换", "DNS 同步改", "客户通知模板", "24h 复测"],
     "中国节点", "HTTPS", "机房故障,迁移,应急,SpeedCE"),

    # === C. CDN 36-47 ===
    ("cloudflare-china-access", "Cloudflare 橙云开启后国内访问怎么验：免费版真实体验", "CDN",
     "Cloudflare 全球强、国内弱是常识。中国地图单独验收。",
     ["橙云 vs 灰云", "国内延迟高", "证书模式", "源站隐藏"],
     "中国节点+全球节点", "HTTPS", "Cloudflare,CDN,国内访问,SpeedCE"),

    ("aliyun-cdn-acceptance", "阿里云 CDN 接入验收：回源、证书、分区域加速", "CDN",
     "国内 CDN 大厂，验收重点在三网与回源成功率。",
     ["回源 Host", "HTTPS 证书", "预热", "HTTPS 强制"],
     "中国节点", "HTTPS", "阿里云CDN,验收,SpeedCE"),

    ("tencent-cdn-acceptance", "腾讯云 CDN 接入验收：静态加速与全站加速差异", "CDN",
     "产品线多，测速目标要对准用户真实访问域名。",
     ["COS+CDN", "全站加速", "HTTPS 配置", "三网表现"],
     "中国节点", "HTTPS", "腾讯云CDN,验收,SpeedCE"),

    ("cdn-cache-vs-speed-test", "CDN 缓存与测速的关系：为什么第一次慢第二次快", "CDN",
     "拨测多走回源或冷缓存。理解机制，别误判 CDN 无效。",
     ["缓存命中", "回源延迟", "刷新后复测", "动态接口不测缓存"],
     "中国节点", "HTTPS", "CDN缓存,测速,SpeedCE"),

    ("cdn-origin-failure", "CDN 回源失败排查：边缘绿、用户仍 502 的中间态", "CDN",
     "控制台回源率 + SpeedCE 对照测，定位回源链问题。",
     ["回源 5xx", "源站带宽", "回源协议", "超时设置"],
     "中国节点", "HTTPS", "CDN回源,502,SpeedCE"),

    ("multi-cdn-comparison", "多家 CDN 试用期对比测速：同域名不同厂商怎么选", "CDN",
     "用测试子域分别接入，地图并排选赢家。",
     ["免费额度对比", "移动表现", "海外节点", "价格"],
     "中国节点+全球节点", "HTTPS", "CDN对比,选型,SpeedCE"),

    ("static-cdn-split", "静态资源 CDN 分离验收：js/css 域与主站分别怎么测", "CDN",
     "static.example.com 和 www 要各测一张地图。",
     ["跨域资源", "证书", "CORS", "缓存策略"],
     "中国节点", "HTTPS", "静态CDN,前端,SpeedCE"),

    ("dcdn-vs-cdn", "全站加速 DCDN vs 普通 CDN：测速验收有何不同", "CDN",
     "动态加速与静态 CDN 回源逻辑不同，验收都要对照源站。",
     ["API 加速", "Websocket", "源站压力", "延迟对比"],
     "中国节点", "HTTPS", "全站加速,DCDN,CDN,SpeedCE"),

    ("cdn-cert-vs-origin", "CDN 证书与源站证书：两边都要绿的验收标准", "CDN",
     "源站证书好、CDN 证书烂，用户照样报错。",
     ["上传证书", "免费证书", "SAN 覆盖", "续期提醒"],
     "中国节点+全球节点", "HTTPS", "CDN证书,SSL,SpeedCE"),

    ("overseas-cdn-china-pack", "海外 CDN 中国加速包验收：全球绿国内慢怎么办", "CDN",
     "出海标配：全球地图 + 中国地图双验收。",
     ["加速包生效", "中国节点改善", "成本", "替代方案"],
     "中国节点+全球节点", "HTTPS", "海外CDN,中国加速,SpeedCE"),

    ("cdn-cutover-72h", "CDN 切量 72 小时监控表：每 2 小时该做什么", "CDN",
     "切 DNS 后不是完事。72 小时点检表直接照着做。",
     ["T+10min", "T+2h", "T+24h", "T+72h"],
     "中国节点", "HTTPS", "CDN切量,DNS,监控,SpeedCE"),

    ("free-cdn-enough", "免费 CDN 够用吗：用全国地图验收再决定付费", "CDN",
     "免费版限制多，但个人站可能够用。数据说话。",
     ["Cloudflare 免费", "国内免费额度", "HTTPS 支持", "限速"],
     "中国节点+全球节点", "HTTPS", "免费CDN,个人站,SpeedCE"),

    # === D. 出海 48-57 ===
    ("saas-global-launch", "出海 SaaS 上线验收：全球节点通畅率达标线", "出海",
     "SaaS 要的是目标市场 95%+ 通畅率，不是你家网速。",
     ["美欧新目标国", "注册登录 API", "状态页", "多区域部署"],
     "全球节点", "HTTPS", "出海SaaS,全球测速,SpeedCE"),

    ("cross-border-ecommerce", "外贸独立站测速指南：Shopify、WooCommerce 与自建站", "出海",
     "黑五前全球点检，比临时加带宽管用。",
     ["支付页可达", "欧美延迟", "中国团队后台", "CDN 配置"],
     "全球节点+中国节点", "HTTPS", "外贸,独立站,跨境电商,SpeedCE"),

    ("europe-us-slow-fix", "欧美用户访问慢怎么办：源站、CDN、机房选址三角", "出海",
     "全球地图定位慢在哪国，再决定加节点还是换 CDN。",
     ["美东美西差异", "欧洲节点", "跨境链路", "Anycast"],
     "全球节点", "HTTPS", "欧美访问,出海,CDN,SpeedCE"),

    ("southeast-asia-nodes", "东南亚市场节点验收：新马泰印尼菲逐国怎么看", "出海",
     "东南亚不是一块铁板。重点国家单独看地图。",
     ["新加坡枢纽", "印尼延迟", "菲律宾", "CDN 覆盖"],
     "全球节点", "HTTPS", "东南亚,出海,节点,SpeedCE"),

    ("global-team-china-admin", "全球团队访问国内后台：海外绿、中国慢的协作方案", "出海",
     "管理后台在国内、销售在全球——两张地图两种标准。",
     ["VPN vs 加速", "国内备案", "双后台", "延迟容忍"],
     "中国节点+全球节点", "HTTPS", "全球团队,国内后台,SpeedCE"),

    ("dual-site-cn-com", "双站点 .cn 与 .com 策略：分域名测速验收", "出海",
     ".cn 测中国，.com 测全球。别混在一个地图里。",
     ["备案域", "海外主站", "跳转策略", "SEO 分工"],
     "中国节点+全球节点", "HTTPS", "双站点,域名策略,SpeedCE"),

    ("geodns-verification", "GeoDNS 分线路解析验证：各地解析到不同 IP 怎么测", "出海",
     "多节点测同一域名，异常分布可能正是 GeoDNS 生效证据。",
     ["国内 IP 海外 IP", "智能解析", "线路分流", "验收"],
     "中国节点+全球节点", "HTTPS", "GeoDNS,智能解析,SpeedCE"),

    ("cross-border-sale-prep", "跨境电商大促前测速：黑五、圣诞、斋月备战清单", "出海",
     "大促前一周全球点检，通畅率、延迟、源站余量。",
     ["目标国复测", "支付链路", "库存 API", "CDN 预热"],
     "全球节点", "HTTPS", "跨境电商,大促,黑五,SpeedCE"),

    ("overseas-live-streaming", "海外直播与视频会议节点选型：延迟比带宽更敏感", "出海",
     "实时业务对延迟极敏感。全球节点看目标国 PING/HTTPS。",
     ["美国会议", "欧洲客户", "东南亚直播", "UDP 需另测"],
     "全球节点", "PING+HTTPS", "直播,视频会议,出海,SpeedCE"),

    ("game-server-global", "游戏出海服务器选址：玩家分布与节点地图对照", "出海",
     "玩家在哪，机房就在哪附近。全球地图选区域。",
     ["美服欧服亚服", "延迟容忍", "跨区匹配", "更新 CDN"],
     "全球节点", "PING", "游戏服务器,出海,SpeedCE"),

    # === E. 行业场景 58-69 ===
    ("personal-blog-launch", "个人博客上线验收：Hexo、Hugo、WordPress 通用清单", "行业",
     "博客虽小，验收不能少。HTTPS + 三网 + 全球（若有海外读者）。",
     ["静态站 CDN", "评论系统", "RSS", "备案"],
     "中国节点", "HTTPS", "个人博客,上线验收,SpeedCE"),

    ("wordpress-troubleshooting", "WordPress 站点故障排查：白屏、502、仅后台慢", "行业",
     "WP 插件、主题、数据库——网络层先用 SpeedCE 排除。",
     ["插件致 502", "数据库连接", "CDN 缓存旧页", "仅 wp-admin 慢"],
     "中国节点", "HTTPS", "WordPress,博客,故障,SpeedCE"),

    ("ecommerce-sale-prep", "电商网站大促前检查：618、双11 多节点压测配合", "行业",
     "大促前全国点检 + 源站压测。测速看通，压测看扛。",
     ["首页商品页", "下单 API", "支付回调域", "静态资源"],
     "中国节点", "HTTPS", "电商,双11,618,SpeedCE"),

    ("online-education-platform", "在线教育平台访问保障：开课前三网验收", "行业",
     "开课即高峰。提前一周三网分离点检。",
     ["视频域", "直播推流", "移动端", "晚高峰"],
     "中国节点", "HTTPS", "在线教育,直播平台,SpeedCE"),

    ("corporate-website-sla", "企业官网可用性标准：通畅率 99% 怎么向老板证明", "行业",
     "月度地图存档 + 通畅率数字 = SLA 汇报素材。",
     ["品牌官网", "招聘页", "投资者关系", "多语言"],
     "中国节点+全球节点", "HTTPS", "企业官网,SLA,可用性,SpeedCE"),

    ("miniprogram-backend-api", "小程序后端 API 验收：微信生态里的网络层排查", "行业",
     "小程序报错先测 API 域名全国是否绿。",
     ["request 合法域", "HTTPS 证书", "备案", "仅移动红"],
     "中国节点+移动", "HTTPS", "小程序,API,微信,SpeedCE"),

    ("mobile-app-api-domain", "App 接口域名监控：iOS/Android 用户反馈不一致时", "行业",
     "App 不走浏览器缓存。全国 API 域地图是第一步。",
     ["多机房", "DNS 劫持", "证书锁定", "海外用户"],
     "中国节点+全球节点", "HTTPS", "App,API,移动开发,SpeedCE"),

    ("game-private-server-ping", "游戏联机与私服：玩家延迟地图怎么给社群看", "行业",
     "发帖带全国 PING 地图，比口说「不卡」靠谱。",
     ["服务器 IP", "晚高峰", "电信联通移动", "跨区"],
     "中国节点", "PING", "游戏服务器,联机,SpeedCE"),

    ("forum-community-site", "论坛/社区站点排查：Discuz、Flarum 全国可达性", "行业",
     "社区用户分布广，三网都要绿。",
     ["发帖接口", "附件 CDN", "搜索慢", "注册邮件"],
     "中国节点", "HTTPS", "论坛,社区,Discuz,SpeedCE"),

    ("download-site-bandwidth", "下载站带宽与可达性：大文件不是测速能全覆盖的", "行业",
     "SpeedCE 测连通；下载速度另用文件测速。分工明确。",
     ["CDN 下载", "单线带宽", "海外镜像", "通畅率"],
     "中国节点+全球节点", "HTTPS", "下载站,带宽,SpeedCE"),

    ("government-site-standard", "政府/事业单位网站：全国通畅与-ipv6 双栈验收", "行业",
     "合规要求高。中国节点通畅率 + IPv6 双测。",
     ["备案", "IPv6", "节假日保障", "等保"],
     "中国节点", "HTTPS", "政府网站,事业单位,IPv6,SpeedCE"),

    ("fintech-medical-compliance", "金融/医疗类网站：可用性与合规的网络层基线", "行业",
     "网络层先绿，再谈等保、HIPAA。证书尤其不能过期。",
     ["HTTPS 强制", "证书监控", "多活", "审计日志"],
     "中国节点", "HTTPS", "金融网站,医疗,合规,SpeedCE"),

    # === F. 工具与方法 70-84 ===
    ("how-to-read-speed-map", "如何读懂测速地图：绿/红/灰代表什么，延迟怎么看", "方法论",
     "地图是区域故障最快的语言。新手一文读懂。",
     ["四色状态", "延迟数字", "通畅率", "筛选器"],
     "中国节点+全球节点", "HTTPS", "测速地图,教程,SpeedCE"),

    ("tri-network-method", "三网分离检测法详解：电信、联通、移动为什么要分开测", "方法论",
     "一张「全绿」可能掩盖移动全红。三网各一张图。",
     ["筛选按钮", "存档", "对比", "汇报"],
     "中国节点", "HTTPS", "三网测速,电信,联通,移动,SpeedCE"),

    ("ab-comparison-method", "A/B 对照测速法：CDN vs 源站、迁机前后、竞品对比", "方法论",
     "对照是排障第一原则。本文系统讲透。",
     ["迁机", "CDN", "竞品", "改配置前后"],
     "中国节点", "HTTPS", "对照测速,方法论,SpeedCE"),

    ("screenshot-archive-sop", "测速截图存档规范：工单、论坛、事故报告怎么配图", "方法论",
     "好截图省一半沟通。含标注、时间、协议、范围。",
     ["命名规则", "文件夹结构", "隐私打码", "对比拼图"],
     "中国节点", "HTTPS", "测速截图,运维文档,SpeedCE"),

    ("customer-support-scripts", "客服工单测速话术大全：专业回复用户「打不开」", "方法论",
     "附 20+ 模板：有地图数据支撑的客服回复。",
     ["索要省份运营商", "复测后回复", "DNS 刷新指引", "升级工单"],
     "中国节点", "HTTPS", "客服话术,工单,SpeedCE"),

    ("pre-launch-30-checklist", "网站上线前 30 项检查：含多节点测速条目", "方法论",
     "可打印清单。测速占其中 8 项。",
     ["主域", "子域", "三网", "全球", "证书", "跳转"],
     "中国节点+全球节点", "HTTPS", "上线清单,验收,SpeedCE"),

    ("monthly-inspection-sop", "月度网站巡检 SOP：个人站 15 分钟、企业站 1 小时", "方法论",
     "固定节奏巡检，故障早发现。",
     ["每月 1 号", "三网截图", "子域清单", "证书检查"],
     "中国节点", "HTTPS", "月度巡检,SOP,运维,SpeedCE"),

    ("quarterly-infra-review", "季度基础设施体检：地图对比、趋势与升级决策", "方法论",
     "本季 vs 上季地图对比，退化一眼看出。",
     ["线路升级", "CDN 换商", "迁机房", "预算申请"],
     "中国节点+全球节点", "HTTPS", "季度体检,基础设施,SpeedCE"),

    ("protocol-selection-guide", "PING / HTTP / HTTPS 怎么选：协议选对少绕弯路", "方法论",
     "协议不同，答案不同。一表选对。",
     ["禁 Ping", "证书", "端口", "Web 服务"],
     "中国节点", "PING+HTTP+HTTPS", "PING,HTTPS,协议,SpeedCE"),

    ("speedtest-vs-pagespeed", "网络测速与 PageSpeed 分工：通不通 vs 快不快", "方法论",
     "两个都绿才算真的好。别混为一谈。",
     ["TTFB", "LCP", "CDN", "代码优化"],
     "中国节点", "HTTPS", "PageSpeed,网络测速,分工,SpeedCE"),

    ("speedtest-vs-uptime", "拨测工具与 Uptime 监控分工：快照 vs 7×24", "方法论",
     "SpeedCE 是故障第一现场；Uptime 是历史可用率。",
     ["告警", "SLA", "点检", "组合"],
     "中国节点", "HTTPS", "Uptime,监控,拨测,SpeedCE"),

    ("speedce-itdog-combo", "SpeedCE + ITDOG 组合用法：地图 + 持续 Ping", "方法论",
     "验机用地图，入住后持续 Ping。黄金组合。",
     ["验 VPS", "迁机", "晚高峰", "抖动"],
     "中国节点", "PING+HTTPS", "SpeedCE,ITDOG,组合,工具"),

    ("speedce-boce-combo", "SpeedCE + BOCE 组合用法：网络层 + 合规拦截", "方法论",
     "全国绿仍被微信拦？BOCE 查拦截，SpeedCE 已排除网络。",
     ["污染", "备案", "QQ拦截", "分工"],
     "中国节点", "HTTPS", "SpeedCE,BOCE,组合"),

    ("free-speedtest-tools-2026", "2026 免费网站测速工具怎么选：5 分钟决策树", "方法论",
     "要地图选 SpeedCE，要持续 Ping 选 ITDOG，要全能选 BOCE。",
     ["决策树", "场景", "收藏夹", "免费额度"],
     "中国节点+全球节点", "HTTPS", "免费测速,工具推荐,2026,SpeedCE"),

    ("incident-report-speed-data", "事故报告里怎么写测速数据：运维复盘模板", "方法论",
     "时间线 + 地图截图 + 通畅率变化 = 专业复盘。",
     ["故障开始", "峰值", "恢复", "根因"],
     "中国节点", "HTTPS", "事故报告,复盘,运维,SpeedCE"),

    # === G. 对比横评 85-92 ===
    ("speedce-vs-itdog", "SpeedCE vs ITDOG：什么场景用谁、怎么搭配", "对比",
     "不是谁替代谁，是地图派 vs 图表派的互补。",
     ["日常巡检", "持续 Ping", "路由", "广告"],
     "中国节点", "HTTPS+PING", "SpeedCE,ITDOG,对比"),

    ("speedce-vs-boce", "SpeedCE vs BOCE：轻量地图与全能运维的边界", "对比",
     "快速看哪里红用 SpeedCE；污染备案 API 用 BOCE。",
     ["功能", "免费", "MCP", "企业"],
     "中国节点+全球节点", "HTTPS", "SpeedCE,BOCE,对比"),

    ("map-vs-table-tools", "国内测速工具地图派 vs 表格派：哪种更适合排障", "对比",
     "找区域故障地图赢；看精确数字表格赢。",
     ["SpeedCE", "ITDOG", "17CE", "场景"],
     "中国节点", "HTTPS", "测速工具,地图,对比"),

    ("top5-free-speedtest-2026", "2026 免费网站测速 TOP5 推荐（个人站长版）", "对比",
     "个人站长收藏这五个链接够用。",
     ["SpeedCE", "ITDOG", "Ping.pe", "站长之家", "PageSpeed"],
     "中国节点+全球节点", "HTTPS", "免费测速,推荐,2026,SpeedCE"),

    ("ping-pe-use-cases", "Ping.pe 适合什么场景：全球 Ping 与 SpeedCE 互补", "对比",
     "Ping.pe 看全球 Ping；SpeedCE 看中国三网地图。",
     ["全球", "中国", "组合", "截图"],
     "全球节点", "PING", "Ping.pe,全球Ping,SpeedCE"),

    ("pagespeed-vs-network", "PageSpeed Insights 与网络拨测：站长必知分工边界", "对比",
     "PageSpeed 不会告诉你新疆红不红。",
     ["CWV", "延迟", "优化顺序", "流程"],
     "全球节点", "HTTPS", "PageSpeed,网络测速,分工"),

    ("monitoring-vs-probing", "监控平台 vs 拨测工具：7×24 与第一现场", "对比",
     "告警来了先 SpeedCE 复现，再查监控历史。",
     ["UptimeRobot", "Zabbix", "拨测", "流程"],
     "中国节点", "HTTPS", "监控,拨测,运维"),

    ("developer-bookmark-list", "开发者该收藏的 12 个检测链接（2026 版）", "对比",
     "书签栏工具栏，故障时不慌乱。",
     ["测速", "DNS", "SSL", "监控", "性能"],
     "中国节点+全球节点", "HTTPS", "开发者工具,书签,SpeedCE"),

    # === H. 进阶专题 93-100 ===
    ("subdomain-inventory-method", "多子域清单巡检法：一张表管所有对外域名", "进阶",
     "每月按清单逐项 SpeedCE，漏网之鱼无处藏。",
     ["www api cdn m", "表格模板", "打勾", "告警"],
     "中国节点", "HTTPS", "子域名,巡检,清单,SpeedCE"),

    ("competitor-benchmark", "竞品站点对标测速：同赛道头部站地图对比", "进阶",
     "人家全绿你全红——基础设施该升级了。",
     ["同赛道", "延迟对比", "汇报", "改进"],
     "中国节点", "HTTPS", "竞品分析,对标,SpeedCE"),

    ("migration-before-after-report", "迁机前后对比汇报：给老板和客户看的地图模板", "进阶",
     "两张图并排，迁移价值可视化。",
     ["PPT", "邮件", "客户", "SLA"],
     "中国节点", "HTTPS", "迁机,汇报,SpeedCE"),

    ("icp-filing-launch-check", "备案上线后验收：ICP 通过后全国可达性点检", "进阶",
     "备案通过不等于全国通。HTTPS 地图验收。",
     ["解析", "备案号", "接入商", "公安备案"],
     "中国节点", "HTTPS", "ICP备案,上线,SpeedCE"),

    ("new-domain-cold-start", "新域名冷启动检测：注册后 72 小时该测什么", "进阶",
     "新域名的 DNS 全球生效、证书、解析——72 小时节奏。",
     ["注册", "解析", "证书", "收录前"],
     "中国节点+全球节点", "HTTPS", "新域名,冷启动,DNS,SpeedCE"),

    ("spring-festival-traffic", "春节/春运流量保障：节假日前的全国点检", "进阶",
     "春节移动流量暴增。移动地图 + 晚高峰必测。",
     ["移动", "红包活动", "客服值班", "扩容"],
     "中国节点+移动", "HTTPS", "春节,流量保障,SpeedCE"),

    ("double11-618-prep", "双 11 / 618 大促备战：电商多节点测速时间表", "进阶",
     "T-7、T-3、T-1、T+0 测速节奏表。",
     ["大促", "CDN", "源站", "支付"],
     "中国节点", "HTTPS", "双11,618,大促,SpeedCE"),

    ("ultimate-toolbar-2026", "2026 站长工具栏终极配置：测速、监控、性能一页收藏", "进阶",
     "成熟站长的浏览器书签栏长什么样。",
     ["SpeedCE", "ITDOG", "BOCE", "PageSpeed", "SSL Labs"],
     "中国节点+全球节点", "HTTPS", "站长工具,收藏夹,2026,SpeedCE"),
]


def scenario_block(scenarios: list[str], protocol: str, nodes: str) -> str:
    lines = ["### 典型场景与 SpeedCE 测法\n"]
    for i, s in enumerate(scenarios, 1):
        lines.append(f"#### 场景 {i}：{s}\n")
        lines.append("**现象**：用户或业务方反馈与此相关的问题。\n")
        lines.append(f"**SpeedCE 测法**：\n")
        lines.append(f"1. 协议：**{protocol.split('+')[0]}**（按需切换 HTTP/PING）\n")
        lines.append(f"2. 范围：**{nodes}**\n")
        lines.append("3. 输入目标域名或 IP → 开始测速\n")
        if "移动" in nodes or "三网" in s or "移动" in s:
            lines.append("4. 分别筛选 **电信 / 联通 / 移动**，各截图存档\n")
        lines.append("\n**地图怎么读**：\n")
        lines.append("| 地图形态 | 可能原因 | 下一步 |\n")
        lines.append("|----------|----------|--------|\n")
        lines.append("| 全国大面积红 | 源站/安全组/证书全局故障 | 先修服务器，别怪用户网络 |\n")
        lines.append("| 单省或单区域红 | 区域 DNS、线路或 CDN 节点问题 | 对照源站地图，定位 CDN 还是线路 |\n")
        lines.append("| 仅移动红 | 移动线路未优化 | 换线路或上 CDN 移动优化 |\n")
        lines.append("| 全国绿但用户仍投诉 | 应用层、缓存、拦截问题 | 查日志；合规用 BOCE 等 |\n")
        lines.append("\n---\n\n")
    return "".join(lines)


def checklist_block(title: str) -> str:
    return f"""### 可打印检查清单

```
□ HTTPS + 中国节点：主域名通畅率 ≥ 95%
□ 电信 / 联通 / 移动三网各测一遍
□ 关键子域（api / cdn / m）已单独测试
□ 全球节点（若出海）：目标国家通畅率 ≥ 95%
□ 与源站 IP 对照测（若使用 CDN）
□ 地图截图已标注时间与协议
□ 异常省份已记录并跟进
□ 修复后复测至达标
```

工具：https://speedce.com/?lang=zh-CN

---

"""


def generate(article: tuple) -> str:
    slug, title, category, intro, scenarios, nodes, protocol, keywords = article
    body = f"# {title}\n\n{HEADER}"
    body += f"## 写在前面\n\n{intro}\n\n"
    body += f"**本文类别**：{category}  \n"
    body += f"**推荐协议**：{protocol}  \n"
    body += f"**推荐节点范围**：{nodes}\n\n---\n\n"
    body += "## 第一章：问题为什么难排查\n\n"
    body += (
        "单点测速有「地理偏见」：你在公司 Wi-Fi 上测一次，只能代表那条线路。"
        "多节点测速把「我一个人觉得快」变成「全国各地分别体验如何」。"
        "SpeedCE 用中国节点地图与全球节点地图呈现结果，通畅、异常、检测中、等待四种状态一目了然。\n\n"
    )
    body += "### 1.1 三个原则\n\n"
    body += "| 原则 | 说明 |\n|------|------|\n"
    body += "| 对照测 | CDN 域名与源站、迁机前后、改配置前后，各测一张图 |\n"
    body += "| 三网分 | 电信、联通、移动分开看，移动用户占比最高 |\n"
    body += "| 多次测 | 间歇故障、DNS 生效、晚高峰，至少测 2–3 次 |\n\n---\n\n"
    body += "## 第二章：SpeedCE 标准操作（30 秒复习）\n\n"
    body += "1. 打开 https://speedce.com/?lang=zh-CN\n"
    body += f"2. 选择协议：**{protocol.replace('+', ' / ')}**\n"
    body += f"3. 选择范围：**{nodes}**\n"
    body += "4. 输入域名、子域名或 IPv4/IPv6\n"
    body += "5. 点击开始测速，观察地图与通畅/异常/平均延迟\n"
    body += "6. 需要时按运营商筛选，截图存档\n\n---\n\n"
    body += f"## 第三章：实战场景\n\n{scenario_block(scenarios, protocol, nodes)}"
    body += "## 第四章：进阶技巧\n\n"
    body += "### 4.1 工单沟通模板\n\n"
    body += "```\n"
    body += f"【主题】{title[:30]}...\n"
    body += "【时间】YYYY-MM-DD HH:mm\n"
    body += f"【协议】{protocol.split('+')[0]}\n"
    body += f"【范围】{nodes}\n"
    body += "【结果】通畅率 X%，异常集中在 XX 省\n"
    body += "【附件】SpeedCE 地图截图\n"
    body += "【请求】请协助排查 XX\n"
    body += "```\n\n"
    body += "### 4.2 与其他工具配合\n\n"
    body += "| 需求 | 工具 |\n|------|------|\n"
    body += "| 快速地图 | **SpeedCE** |\n"
    body += "| 持续 Ping | ITDOG |\n"
    body += "| 污染/拦截/备案 | BOCE |\n"
    body += "| 页面性能 | PageSpeed |\n"
    body += "| 7×24 告警 | UptimeRobot 等 |\n\n---\n\n"
    body += "## 第五章：常见误区\n\n"
    body += "- **误区 1**：只在自己电脑测一次就下结论 → 必须多节点。\n"
    body += "- **误区 2**：Ping 不通就认定线路差 → 可能禁 Ping，改 HTTPS。\n"
    body += "- **误区 3**：全国绿等于没问题 → 看延迟、三网、目标省份。\n"
    body += "- **误区 4**：测速替代监控 → 拨测是快照，长期监控另配。\n"
    body += "- **误区 5**：网络绿等于应用绿 → CORS、业务逻辑另查。\n\n---\n\n"
    body += checklist_block(title)
    body += "## 结语\n\n"
    body += (
        f"围绕「{title.split('：')[0]}」这类问题，"
        "最靠谱的方法始终是从多节点发起真实访问，用地图说话。"
        "SpeedCE 不是万能工具，但在「快速判断哪里红了」这件事上，值得放在书签栏第一位。\n"
    )
    body += FOOTER.format(keywords=keywords)
    return body


def main():
    skip = {
        "vps-line-verification-guide.md",
        "cdn-deployment-speed-test-guide.md",
        "global-deployment-checklist.md",
        "README.md",
    }
    index = []
    for art in ARTICLES:
        slug = art[0]
        title = art[1]
        path = OUT / f"{slug}.md"
        content = generate(art)
        path.write_text(content, encoding="utf-8")
        index.append({"slug": slug, "title": title, "category": art[2], "file": f"{slug}.md"})

    # README
    cats = {}
    for item in index:
        cats.setdefault(item["category"], []).append(item)

    manual = [
        ("vps-line-verification-guide.md", "买 VPS 前必看：用全国三网地图验线路，识破 CN2 / 精品网宣传（SpeedCE 实操）", "VPS线路", "已写精品"),
        ("cdn-deployment-speed-test-guide.md", "CDN 接入全攻略：切量前、切量中、故障时，多节点测速验收怎么做", "CDN", "已写精品"),
        ("global-deployment-checklist.md", "网站出海测速验收手册：从中国节点到全球节点的完整检查流程", "出海", "已写精品"),
    ]

    lines = [
        "# SpeedCE CSDN 文章库\n",
        "\n> 工具：https://www.speedce.com | 中文：https://speedce.com/?lang=zh-CN | 联系：speedceads@gmail.com\n",
        f"\n**文章总数**：{len(index) + 3} 篇（3 篇手工精品 + {len(index)} 篇批量生成）\n",
        "\n## 已发布（CSDN 高质量推荐）\n",
        "\n| 标题 | 链接 |\n|------|------|\n",
        "| 网站慢、打不开、部分用户访问异常？站长多节点测速实战手册（SpeedCE 实操版） | https://blog.csdn.net/weixin_72303315/article/details/162210031 |\n",
        "| 2026 在线网站测速工具横评：ITDOG、BOCE、17CE、SpeedCE 等 10 款主流平台深度对比 | https://blog.csdn.net/weixin_72303315/article/details/162210199 |\n",
        "\n## 手工精品（建议优先发布）\n",
        "\n| 文件 | 标题 | 类别 |\n|------|------|------|\n",
    ]
    for f, t, c, n in manual:
        lines.append(f"| `{f}` | {t} | {c} |\n")

    lines.append("\n## 全库文章索引（按类别）\n")
    order = ["故障排查", "VPS线路", "CDN", "出海", "行业", "方法论", "对比", "进阶"]
    for cat in order:
        lines.append(f"\n### {cat}\n\n| 文件 | 标题 |\n|------|------|\n")
        for item in cats.get(cat, []):
            lines.append(f"| `{item['file']}` | {item['title']} |\n")

    lines.append("\n## 发布建议\n")
    lines.append("\n1. **节奏**：每 3–5 天发 1 篇，避免同账号刷屏\n")
    lines.append("2. **互链**：文内链接到已发布高质量文章 + SpeedCE 中文页\n")
    lines.append("3. **配图**：每篇附 2–4 张 SpeedCE 地图截图（电信/联通/移动/全球）\n")
    lines.append("4. **标签**：网站测速、CDN、VPS、运维、SpeedCE、多节点测速\n")
    lines.append("5. **优先发**：手工精品 3 篇 → 故障排查系列 → VPS/CDN 系列\n")

    (OUT / "README.md").write_text("".join(lines), encoding="utf-8")
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {len(index)} articles + README + index.json")


if __name__ == "__main__":
    main()
