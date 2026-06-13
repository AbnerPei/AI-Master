---
创建日期: 2026-06-12T12:54:13
来源: 视频号
人物: 傅盛讲AI
seed: https://weixin.qq.com/sph/At1xESEPjT
状态: partial
---

# 傅盛讲AI：创作者内容枚举

## 本次结论

- 枚举状态：`partial`
- 已发现条目数：`1`
- 是否已知全量总数：`False`
- 覆盖说明：本次结果只能确认 seed 视频已存在，不代表已拿到该创作者全部视频。

## 创作者身份

- 名称：`傅盛讲AI`
- 主页链接：[https://channels.weixin.qq.com/finder-preview/pages/sph?id=At1xESEPjT](https://channels.weixin.qq.com/finder-preview/pages/sph?id=At1xESEPjT)
- 身份状态：`provisional`
- 身份说明：当前公开单条 feed 接口未返回稳定的创作者主键，先以可见名称建立暂存身份。

## 当前条目

- 标题：`AI黑客松大赛让人震惊，初中生近乎夺冠，中国版盖茨快出现了#跟傅盛学AI#AI编程#VibeCoding#猎豹移动#黑客马拉松`
- 来源链接：[https://channels.weixin.qq.com/finder-preview/pages/sph?id=At1xESEPjT](https://channels.weixin.qq.com/finder-preview/pages/sph?id=At1xESEPjT)
- 发布时间：`2026-01-28T17:11:33+08:00`
- 时间精度：`exact`
- 队列状态：`metadata-only`
- 下载状态：`missing`

## 策略轨迹

### feed_info_api
- 类型：`public-response`
- 优先级：`1`
- 状态：`success`
- 说明：通过单条 `shortUri` 接口拿到 seed 视频元数据和可见作者名称。

### public_seed_page
- 类型：`public-page`
- 优先级：`2`
- 状态：`success`
- 说明：当前公开 seed 页面是前端壳页，未直接内嵌创作者全量内容列表。

### public_creator_catalog
- 类型：`public-catalog`
- 优先级：`3`
- 状态：`unavailable`
- 说明：当前公开 seed 页面和单条 feed 接口都没有暴露稳定的创作者全量列表入口或创作者主键。

### mac_wechat_automation
- 类型：`desktop-fallback`
- 优先级：`4`
- 状态：`required`
- 说明：若要追求创作者全量遍历，需要在 `Mac WeChat` 中做主页级或列表级自动化，而不是人工逐条点开。

## 失败原因

- 当前公开 seed 页面仅暴露前端壳页，未直接给出创作者全量内容列表。
- 当前公开单条 feed 接口能确认 seed 视频，但未给出稳定的创作者全量枚举主键。

## 后续动作

- 继续尝试从后续网页 bundle 或响应里定位创作者主页级接口。
- 如果公开路径仍不足，则转入 `Mac WeChat` 主页级自动化遍历。
- 对已发现条目逐步补齐本地视频、副标题、转写稿和发布时间复核。
