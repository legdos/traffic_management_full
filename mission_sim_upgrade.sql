-- ============================================================
-- 马表仿真：mission 表结构升级
-- 适用：MariaDB 10.4 / MySQL 5.7+（ADD COLUMN IF NOT EXISTS 为 MariaDB 语法）
-- 幂等：重复执行不会报错、不会重复加列
-- 执行前建议先备份：
--   mysqldump -h 127.0.0.1 -P 3306 -u root --databases traffic --result-file=traffic_backup.sql
-- ============================================================

ALTER TABLE `mission`
  ADD COLUMN IF NOT EXISTS `dest_factory_id` int(11)   DEFAULT NULL COMMENT '终点工厂'      AFTER `factory_id`,
  ADD COLUMN IF NOT EXISTS `goods_type`      varchar(50) DEFAULT NULL COMMENT '货物类型'      AFTER `goods_id`,
  ADD COLUMN IF NOT EXISTS `distance_km`     double      DEFAULT 0    COMMENT '起点到终点距离(km)' AFTER `totalVol`,
  ADD COLUMN IF NOT EXISTS `total_minutes`   int(11)     DEFAULT 0    COMMENT '任务总耗时(分钟)' AFTER `distance_km`,
  ADD COLUMN IF NOT EXISTS `elapsed_minutes` int(11)     DEFAULT 0    COMMENT '已耗时(分钟)'    AFTER `total_minutes`;

-- 验证
-- DESCRIBE mission;
