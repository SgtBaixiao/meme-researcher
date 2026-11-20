# 证据文件契约

每项来源与论断使用稳定的 ID。来源链表示内容的共同出处：转载和原帖使用相同的值；两个来源是否独立，由研究记录说明。

```json
{
  "sources": [
    {"id": "source-a", "url": "https://example.org/original", "origin_chain": "original-a"},
    {"id": "source-b", "url": "https://example.net/independent", "origin_chain": "original-b"}
  ],
  "claims": [
    {"id": "claim-a", "text": "待填写的研究论断", "source_ids": ["source-a", "source-b"], "status": "confirmed"}
  ]
}
```

示例地址和文本只演示格式，不是实际证据。确认状态需要两个已声明的独立来源链。其他状态为 `community-research`、`rumor` 和 `unverified`，对应网友考证、流传说法和待考证；尚无来源的待考证论断可使用空引用数组。

来源可附标题、作者、日期、原文文件路径及独立性说明，校验工具保留这些字段。机器只验证结构、引用和来源链数量，报告的事实核查仍由研究员与用户完成。
