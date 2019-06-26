# Relase Notes

## 1.0.0

- 简单的查询语句绘制图表
  目前仅支持一张图表二维表示，如查询最近 7 天的总事件数
  ```sql
  SELECT DATE_FORMAT(DATE(created_at), "%Y-%m-%d"), COUNT(*) FROM events WHERE DATE(created_at) BETWEEN DATE(NOW())-6 AND DATE(now()) GROUP BY DATE(created_at);
  ```
- 创建新查询时图表预览和提交
- 保存历史创建图表于首页