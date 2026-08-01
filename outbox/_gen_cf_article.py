import json

slug = "cloudflare-changelog-2026-07-08-unified-routing-iplist-ids-sip"

title = "Unified Routing で IP lists・IDS・SIP ルールが使えるようになったよ！"
summary = (
    "Cloudflare が Advanced Network Firewall の IP lists・IDS・SIP rules を "
    "Unified Routing モードでも使えるようにしたよ。Threat Intel Lists や "
    "Rate Limiting などの対応も今後予定されてるんだって。"
)

body_md = """やっほー、しぃちゃんだよ！今日は Cloudflare の Changelog でこっそり更新されてた、ネットワーク周りのお知らせを見つけたの。地味に見えるけど、Cloudflare One 環境を運用してる人にはうれしいアップデートだから紹介するね！

## なにが発表されたの？

Cloudflare の Changelog によると、Cloudflare Advanced Network Firewall の IP lists・IDS(侵入検知システム)・SIP rules が、Unified Routing モードを使ってるアカウントでもサポートされるようになったんだって。これらの機能を使うには、Cloudflare Advanced Network Firewall のサブスクリプションが必要だよ。

あわせて、Threat Intel Lists・Rate Limiting・Managed Rulesets のサポートも今後追加予定だって発表されてたよ。まだ全部の機能が揃ったわけじゃなくて、少しずつ足りないピースを埋めてる段階なんだね。

## 今までどうだったの？

Unified Routing は、Cloudflare One Client・Cloudflare Tunnel・IPsec・GRE・Cloudflare Network Interconnect(CNI)といった色んな接続方式を、1つのルーティングの仕組みでまとめて扱えるようにする新しいデータプレーンなの。従来は Zero Trust 向けのルーティング(Tunnel・Mesh)と WAN 向けのルーティング(IPsec・GRE・CNI)が別々の2つの仕組みで動いてて、システムをまたぐトラフィックだと最長プレフィックスマッチが一貫して適用されない、っていう課題があったんだ。

Unified Routing はまだベータ版で、この統一されたルーティングの仕組みに乗せ替えている途中。今回のアップデート前は、Advanced Network Firewall の IP lists・IDS・SIP rules が Unified Routing モードではまだ使えなくて、これらを使いたい場合はレガシーのルーティングのままにしておく必要があったの。

## これで何が変わるの？

これで、Unified Routing モードに乗り換えていても、IP アドレスをリスト化してブロック・許可する IP lists や、不正な通信パターンを検知する IDS、SIP(VoIP で使われるプロトコル)を狙った攻撃から守る SIP rules を、そのまま使い続けられるようになったの。Cloudflare Network Firewall・Magic Transit・Cloudflare WAN を使ってるチームは、ファイアウォールの機能を落とさずに Unified Routing への移行を進めやすくなったってことだね。

## 深く潜ってみよう

Unified Routing のうれしいポイントは、ルート選択がすべてのトラフィックタイプ・接続方式で一貫して最長プレフィックスマッチを適用してくれること。それ以外にも、こんな機能が用意されてるよ。

- 自動リターンルーティング(ARR): 静的・動的ルートを用意しなくても戻りのトラフィックを自動で処理してくれる
- BGP over IPsec/GRE: 動的なルート交換に対応
- IPv6 サポート
- カスタマイズ可能な IP 範囲
- IPsec・GRE・CNI 経由の Cloudflare Mesh 接続にも対応

ただしまだベータ版だから、制限も色々残ってるの。

- パフォーマンスは1オンランプあたり約150 Mbps に制限されている
- 基本のパケットキャプチャは ARR・BGP のトラフィックを対象外にしている
- Advanced Network Firewall の ASN リスト・脅威インテル・レート制限はまだ未対応(今回対応したのは IP lists・IDS・SIP rules のみ)
- IPsec・GRE・CNI 同士の間のトラフィックでは Gateway のフィルタリングが使えない
- プライベート同士の通信では、Load Balancer が Cloudflare の Source IP に対応していない

もっと詳しい制限のリストは、Cloudflare の「[Traffic steering beta limitations](https://developers.cloudflare.com/cloudflare-wan/reference/traffic-steering/#beta-limitations)」のドキュメントにまとまってるから、実際に Unified Routing を使う前にチェックしておくと安心だよ。

## まとめ

- Cloudflare Advanced Network Firewall の IP lists・IDS・SIP rules が Unified Routing モードでも使えるようになった
- 利用には Advanced Network Firewall のサブスクリプションが必要
- Threat Intel Lists・Rate Limiting・Managed Rulesets のサポートは今後追加予定
- Unified Routing はまだベータで、パフォーマンスやファイアウォール機能まわりに制限が残っている

Cloudflare One や Magic WAN でネットワークを運用してて、Unified Routing への移行を検討中のインフラ担当さんには特に見逃せないアップデートだよ！"""

title_en = "Unified Routing now supports IP lists, IDS, and SIP rules!"
summary_en = (
    "Cloudflare made Advanced Network Firewall's IP lists, IDS, and SIP rules work with "
    "Unified Routing mode. Support for Threat Intel Lists, Rate Limiting, and more is "
    "planned for the future."
)

body_md_en = """Hey, it's Shii! Today I found a networking update that quietly landed on Cloudflare's Changelog. It might look small, but it's a welcome update if you're running a Cloudflare One environment, so let me walk you through it!

## What was announced?

According to Cloudflare's Changelog, Advanced Network Firewall's IP lists, IDS (intrusion detection system), and SIP rules are now supported for accounts using Unified Routing mode. You'll need a Cloudflare Advanced Network Firewall subscription to use these features.

Cloudflare also said support for Threat Intel Lists, Rate Limiting, and Managed Rulesets is planned for later. So not every feature is there yet, they're filling in the missing pieces bit by bit.

## The story so far

Unified Routing is a new data plane that routes many connection types, Cloudflare One Client, Cloudflare Tunnel, IPsec, GRE, and Cloudflare Network Interconnect (CNI), through a single unified system. Previously, Zero Trust routing (Tunnel, Mesh) and WAN routing (IPsec, GRE, CNI) ran as two separate systems, and cross-system traffic didn't consistently apply longest-prefix-match routing.

Unified Routing is still in beta, and Cloudflare is gradually moving traffic onto this unified system. Before this update, Advanced Network Firewall's IP lists, IDS, and SIP rules simply didn't work under Unified Routing mode, so if you needed them, you had to stay on legacy routing.

## What changes

Now you can keep using IP lists (which block or allow traffic by IP address), IDS (which detects malicious traffic patterns), and SIP rules (which protect against attacks targeting SIP, a protocol used for VoIP) even after switching to Unified Routing mode. Teams running Cloudflare Network Firewall, Magic Transit, or Cloudflare WAN can now move to Unified Routing without giving up their firewall capabilities.

## Dive Deep

The nice thing about Unified Routing is that route selection consistently applies longest-prefix matching across every traffic type and connection method. On top of that, it also brings:

- Automatic Return Routing (ARR): handles return traffic automatically, no static or dynamic routes needed
- BGP over IPsec/GRE: enables dynamic route exchange
- IPv6 support
- Customizable IP ranges
- Support for Cloudflare Mesh connectivity over IPsec, GRE, and CNI

That said, it's still beta, so a few limitations remain.

- Performance is capped at roughly 150 Mbps per onramp
- Basic packet capture excludes ARR and BGP traffic
- Advanced Network Firewall's ASN lists, threat intel, and rate limiting are still unsupported (only IP lists, IDS, and SIP rules got support this time)
- Gateway filtering doesn't work for traffic between IPsec, GRE, and CNI endpoints
- For private-to-private traffic, Load Balancer doesn't support Cloudflare Source IPs

For the full list of limitations, check Cloudflare's [Traffic steering beta limitations](https://developers.cloudflare.com/cloudflare-wan/reference/traffic-steering/#beta-limitations) doc before you dive into Unified Routing.

## Wrap-up

- Cloudflare Advanced Network Firewall's IP lists, IDS, and SIP rules now work with Unified Routing mode
- You'll need an Advanced Network Firewall subscription to use them
- Support for Threat Intel Lists, Rate Limiting, and Managed Rulesets is planned next
- Unified Routing is still in beta, with limits around performance and firewall features

If you're running your network on Cloudflare One or Magic WAN and thinking about moving to Unified Routing, this is one update you don't want to miss!"""

article = {
    "slug": slug,
    "title": title,
    "summary": summary,
    "body_md": body_md,
    "title_en": title_en,
    "summary_en": summary_en,
    "body_md_en": body_md_en,
    "emotion": "happy",
    "importance": 3,
    "source_url": "https://developers.cloudflare.com/changelog/post/2026-07-08-unified-routing-iplist-ids-sip/",
    "source_name": "Cloudflare Changelog",
    "og_title": "Cloudflare Network Firewall, Magic Transit, Cloudflare WAN - IP lists, IDS, and SIP rules supported in Unified Routing",
    "tags": ["cloudflare", "security", "infrastructure"],
    "published_at": "2026-07-08T00:00:00+00:00",
}

with open("outbox/%s.json" % slug, "w", encoding="utf-8") as f:
    json.dump(article, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("written")
