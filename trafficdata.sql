/*
Navicat MySQL Data Transfer

Source Server         : 111
Source Server Version : 50505
Source Host           : 127.0.0.1:3306
Source Database       : traffic

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2026-10-27 19:57:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for action
-- ----------------------------
DROP TABLE IF EXISTS `action`;
CREATE TABLE `action` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '行为ID',
  `actionName` varchar(100) NOT NULL COMMENT '行为名称',
  `actionType` varchar(20) DEFAULT NULL COMMENT '行为类型：运输中、卸货、保养',
  `duration` int(11) DEFAULT NULL COMMENT '持续时间（分钟）',
  `accidentRate` decimal(5,2) DEFAULT NULL COMMENT '异常率（%）',
  PRIMARY KEY (`id`),
  KEY `actionName` (`actionName`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of action
-- ----------------------------
INSERT INTO `action` VALUES ('1', '空闲', 'IDLE', '0', '0.00');
INSERT INTO `action` VALUES ('2', '接单行驶', 'ACCEPTING', '5', '0.05');
INSERT INTO `action` VALUES ('3', '装货', 'LOADING', '3', '0.02');
INSERT INTO `action` VALUES ('4', '运货行驶', 'TRANSPORTING', '10', '0.08');
INSERT INTO `action` VALUES ('5', '卸货', 'UNLOADING', '3', '0.02');
INSERT INTO `action` VALUES ('6', '停留等待', 'WAITING', '2', '0.01');
INSERT INTO `action` VALUES ('7', '初始状态', 'INIT', '0', '0.00');

-- ----------------------------
-- Table structure for factory
-- ----------------------------
DROP TABLE IF EXISTS `factory`;
CREATE TABLE `factory` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '工厂ID',
  `factoryName` varchar(50) NOT NULL COMMENT '工厂名称',
  `address` varchar(100) DEFAULT NULL COMMENT '地址',
  `phone` varchar(20) DEFAULT NULL COMMENT '联系电话',
  `createTime` datetime DEFAULT current_timestamp() COMMENT '创建时间',
  `need_id` int(11) DEFAULT NULL,
  `factoryLatitude` double(10,6) DEFAULT NULL,
  `factoryLongitude` double(10,6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ibfk_1` (`need_id`),
  CONSTRAINT `ibfk_1` FOREIGN KEY (`need_id`) REFERENCES `need` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1194 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of factory
-- ----------------------------
INSERT INTO `factory` VALUES ('864', '乐家家具源头工厂', '团结路段32号', '', null, '1', '31.054825', '103.675325');
INSERT INTO `factory` VALUES ('865', '明智酒厂', '府青路241号', '', null, '1', '30.580601', '103.632139');
INSERT INTO `factory` VALUES ('866', '四川金盆地(集团)有限公司新厂', '余塘村村委会南侧290米', '', null, '1', '30.665325', '103.664875');
INSERT INTO `factory` VALUES ('867', '都江堰市鹏辉塑料制品厂', '蒲阳镇双柏社区三组58号', '', null, '1', '31.028863', '103.708112');
INSERT INTO `factory` VALUES ('868', '金盆地酒厂', '金盆地大道与晋康北路交叉口东40米', '', null, '1', '30.648512', '103.685239');
INSERT INTO `factory` VALUES ('869', '金柏莱家居工厂', '正科路169号', '', null, '1', '30.594341', '103.689851');
INSERT INTO `factory` VALUES ('870', '成都超德创科技有限公司', '新园一路39号', '', null, '1', '30.265277', '103.647645');
INSERT INTO `factory` VALUES ('871', 'WEIO卫洛超级代工厂', '沙新路 368 号左转', '', null, '1', '30.515625', '103.741625');
INSERT INTO `factory` VALUES ('872', '成都嘎嘎辣卤工厂', '金马街道尚石路南段159号', '', null, '1', '30.660150', '103.775509');
INSERT INTO `factory` VALUES ('873', '德洛巴顿家具二分厂', '永兴街137号', '', null, '1', '30.845648', '103.817421');
INSERT INTO `factory` VALUES ('874', '诺雅馨钢木家具厂', '画江大道三段与崇新路一段交叉口西南460米', '', null, '1', '30.543824', '103.761515');
INSERT INTO `factory` VALUES ('875', '成温邛扩容项目TJ1标钢筋加工厂', '新南路100号', '', null, '1', '30.712690', '103.824410');
INSERT INTO `factory` VALUES ('876', '四川馨三合食品有限公司', '丹景山镇', '', null, '1', '31.088298', '103.880860');
INSERT INTO `factory` VALUES ('877', '崇州市三江小金鱼皮鞋厂', '崇双大道三段1236号', '', null, '1', '30.576541', '103.811437');
INSERT INTO `factory` VALUES ('878', '彭州市名典家具厂', '天彭镇白马村5组1号', '', null, '1', '30.995675', '103.912925');
INSERT INTO `factory` VALUES ('879', '石材橱柜定制厂家', '濂溪村四组125号', '', null, '1', '30.837895', '103.891185');
INSERT INTO `factory` VALUES ('880', '艾瑞杰铜铝不锈钢打包厂', '鹃兴路与郫彭路交叉口西北480米', '', null, '1', '30.825575', '103.894725');
INSERT INTO `factory` VALUES ('881', '一顶红伞蓬制品厂(源头工厂)', '安信路108-114', '', null, '1', '30.981168', '103.926585');
INSERT INTO `factory` VALUES ('882', '成都政城通风设备有限公司(风管生产厂家)', '郫彭路蓬兴物流中转站内', '', null, '1', '30.849525', '103.909733');
INSERT INTO `factory` VALUES ('883', '鑫怡米粉厂', '九斗渠路', '', null, '1', '30.702679', '103.889182');
INSERT INTO `factory` VALUES ('884', '成都鑫瑞龙机械制造有限公司', '彭镇工业园罗汉路南2段6号', '', null, '1', '30.585275', '103.880475');
INSERT INTO `factory` VALUES ('885', '成都市西园净水厂(市第十一净水厂)', '四川省成都市郫都区', '', null, '1', '30.748875', '103.909975');
INSERT INTO `factory` VALUES ('886', '九洲昌隆高标准智能化农产品加工工厂', '涪陵路286号', '', null, '1', '30.612853', '103.891323');
INSERT INTO `factory` VALUES ('887', '索尔思光电(成都)有限公司-2号标准厂房', '科新路8号附5号', '', null, '1', '30.774657', '103.922418');
INSERT INTO `factory` VALUES ('888', '广东华克思系统门窗厂', '九江镇九洋路4号铝合金门窗重型门折叠门阳光房雨棚葡萄架凉亭踢脚线平开门推拉门极窄门衣柜门极窄隔断系统门窗复古门窗', '', null, '1', '30.638001', '103.912847');
INSERT INTO `factory` VALUES ('889', '岷江水厂牧马山分厂', '云岭路52号', '', null, '1', '30.527646', '103.893869');
INSERT INTO `factory` VALUES ('890', '四川博亿包装有限公司', '现代工业港北片区港通北四路269号', '', null, '1', '30.810295', '103.928467');
INSERT INTO `factory` VALUES ('891', '碳晶板防撞板墙板金属雕花板厂', '红光街道港北二路569号1栋1层1号', '', null, '1', '30.808825', '103.939025');
INSERT INTO `factory` VALUES ('892', '鲁班创美(双流工厂)', '成大路8号', '', null, '1', '30.634872', '103.913750');
INSERT INTO `factory` VALUES ('893', '千咏整装定制家具工厂', '隆丰街道军屯村四组8586号', '', null, '1', '31.060436', '103.985896');
INSERT INTO `factory` VALUES ('894', '顾瑞全屋定制(工厂)', '聚尚美居家具厂东南侧170米', '', null, '1', '30.827572', '103.993712');
INSERT INTO `factory` VALUES ('895', '钧坤锋拓新能源商务车地板厂', '康安路229号', '', null, '1', '30.592829', '103.946448');
INSERT INTO `factory` VALUES ('896', '柯莱恩全屋定制工厂', '成都家具产业园列维士路358号', '', null, '1', '30.857837', '104.013198');
INSERT INTO `factory` VALUES ('897', '方师傅食品厂', '九尺镇宝马村16组74号', '', null, '1', '30.999676', '104.035274');
INSERT INTO `factory` VALUES ('898', '琴悦钢琴批发厂', '铁佛路44号(簇桥地铁站C口步行370米)', '', null, '1', '30.610188', '103.990603');
INSERT INTO `factory` VALUES ('899', '中铁十九局集团大件路改造项目钢筋加工厂', '月星路与西航港大道中三段交叉口东420米', '', null, '1', '30.556295', '103.982077');
INSERT INTO `factory` VALUES ('900', '郫县凯欣服装厂', '方碑街62-3栋附18号', '', null, '1', '30.766168', '104.017033');
INSERT INTO `factory` VALUES ('901', '龙桥陆陆勇制衣厂', '普华路一巷44号', '', null, '1', '30.814428', '104.030196');
INSERT INTO `factory` VALUES ('902', '张熠复合厂', '龙腾大道863号', '', null, '1', '30.814027', '104.034899');
INSERT INTO `factory` VALUES ('903', '成都德笙普集成吊顶厂', '太平园西部家居城5幢B4-5号', '', null, '1', '30.609625', '104.004890');
INSERT INTO `factory` VALUES ('904', '宴池酒厂', '同和路99-附59号', '', null, '1', '30.685097', '104.016576');
INSERT INTO `factory` VALUES ('905', '四川成都佳农宝菜加工厂', '清河村6组150号', '', null, '1', '30.878225', '104.048625');
INSERT INTO `factory` VALUES ('906', '爬山虎窗帘智能工厂', '斑竹园三山路公益10组61号4楼', '', null, '1', '30.827525', '104.049275');
INSERT INTO `factory` VALUES ('907', '四川庆宏电焊网厂', '小普路165号', '', null, '1', '30.805469', '104.049009');
INSERT INTO `factory` VALUES ('908', '成都超纯应用材料股份有限公司新建厂区', '华府大道四段19号', '', null, '1', '30.455883', '104.003368');
INSERT INTO `factory` VALUES ('909', '成都市骑龙净水厂(市第十二净水厂)', '祥华路2910号', '', null, '1', '30.537403', '104.021881');
INSERT INTO `factory` VALUES ('910', '成都钢豪加工厂', '', '', null, '1', '30.733230', '104.051024');
INSERT INTO `factory` VALUES ('911', '成都地奥九泓制造厂', '创业路辅路与九兴大道交叉口西南100米', '', null, '1', '30.618825', '104.041525');
INSERT INTO `factory` VALUES ('912', '成都众森源全屋定制家具厂', '斑竹园镇仁和村民大路978号', '', null, '1', '30.869625', '104.085875');
INSERT INTO `factory` VALUES ('913', '中铁八局成德线二工区钢筋厂', '北星大道一段6408正', '', null, '1', '30.801126', '104.075894');
INSERT INTO `factory` VALUES ('914', '乐家家具源头工厂', '团结路段32号', '', null, '1', '31.054825', '103.675325');
INSERT INTO `factory` VALUES ('915', '四川金盆地(集团)有限公司新厂', '余塘村村委会南侧290米', '', null, '1', '30.665325', '103.664875');
INSERT INTO `factory` VALUES ('916', '都江堰市鹏辉塑料制品厂', '蒲阳镇双柏社区三组58号', '', null, '1', '31.028863', '103.708112');
INSERT INTO `factory` VALUES ('917', '明智酒厂', '府青路241号', '', null, '1', '30.580601', '103.632139');
INSERT INTO `factory` VALUES ('918', '金盆地酒厂', '金盆地大道与晋康北路交叉口东40米', '', null, '1', '30.648512', '103.685239');
INSERT INTO `factory` VALUES ('919', '金柏莱家居工厂', '正科路169号', '', null, '1', '30.594341', '103.689851');
INSERT INTO `factory` VALUES ('920', '成都超德创科技有限公司', '新园一路39号', '', null, '1', '30.265277', '103.647645');
INSERT INTO `factory` VALUES ('921', 'WEIO卫洛超级代工厂', '沙新路 368 号左转', '', null, '1', '30.515625', '103.741625');
INSERT INTO `factory` VALUES ('922', '诺雅馨钢木家具厂', '画江大道三段与崇新路一段交叉口西南460米', '', null, '1', '30.543824', '103.761515');
INSERT INTO `factory` VALUES ('923', '德洛巴顿家具二分厂', '永兴街137号', '', null, '1', '30.845648', '103.817421');
INSERT INTO `factory` VALUES ('924', '成都嘎嘎辣卤工厂', '金马街道尚石路南段159号', '', null, '1', '30.660150', '103.775509');
INSERT INTO `factory` VALUES ('925', '成温邛扩容项目TJ1标钢筋加工厂', '新南路100号', '', null, '1', '30.712690', '103.824410');
INSERT INTO `factory` VALUES ('926', '四川馨三合食品有限公司', '丹景山镇', '', null, '1', '31.088298', '103.880860');
INSERT INTO `factory` VALUES ('927', '崇州市三江小金鱼皮鞋厂', '崇双大道三段1236号', '', null, '1', '30.576541', '103.811437');
INSERT INTO `factory` VALUES ('928', '艾瑞杰铜铝不锈钢打包厂', '鹃兴路与郫彭路交叉口西北480米', '', null, '1', '30.825575', '103.894725');
INSERT INTO `factory` VALUES ('929', '一顶红伞蓬制品厂(源头工厂)', '安信路108-114', '', null, '1', '30.981168', '103.926585');
INSERT INTO `factory` VALUES ('930', '鑫怡米粉厂', '九斗渠路', '', null, '1', '30.702679', '103.889182');
INSERT INTO `factory` VALUES ('931', '成都政城通风设备有限公司(风管生产厂家)', '郫彭路蓬兴物流中转站内', '', null, '1', '30.849525', '103.909733');
INSERT INTO `factory` VALUES ('932', '石材橱柜定制厂家', '濂溪村四组125号', '', null, '1', '30.837895', '103.891185');
INSERT INTO `factory` VALUES ('933', '彭州市名典家具厂', '天彭镇白马村5组1号', '', null, '1', '30.995675', '103.912925');
INSERT INTO `factory` VALUES ('934', '索尔思光电(成都)有限公司-2号标准厂房', '科新路8号附5号', '', null, '1', '30.774657', '103.922418');
INSERT INTO `factory` VALUES ('935', '九洲昌隆高标准智能化农产品加工工厂', '涪陵路286号', '', null, '1', '30.612853', '103.891323');
INSERT INTO `factory` VALUES ('936', '成都鑫瑞龙机械制造有限公司', '彭镇工业园罗汉路南2段6号', '', null, '1', '30.585275', '103.880475');
INSERT INTO `factory` VALUES ('937', '四川博亿包装有限公司', '现代工业港北片区港通北四路269号', '', null, '1', '30.810295', '103.928467');
INSERT INTO `factory` VALUES ('938', '岷江水厂牧马山分厂', '云岭路52号', '', null, '1', '30.527646', '103.893869');
INSERT INTO `factory` VALUES ('939', '成都市西园净水厂(市第十一净水厂)', '四川省成都市郫都区', '', null, '1', '30.748875', '103.909975');
INSERT INTO `factory` VALUES ('940', '广东华克思系统门窗厂', '九江镇九洋路4号铝合金门窗重型门折叠门阳光房雨棚葡萄架凉亭踢脚线平开门推拉门极窄门衣柜门极窄隔断系统门窗复古门窗', '', null, '1', '30.638001', '103.912847');
INSERT INTO `factory` VALUES ('941', '碳晶板防撞板墙板金属雕花板厂', '红光街道港北二路569号1栋1层1号', '', null, '1', '30.808825', '103.939025');
INSERT INTO `factory` VALUES ('942', '鲁班创美(双流工厂)', '成大路8号', '', null, '1', '30.634872', '103.913750');
INSERT INTO `factory` VALUES ('943', '千咏整装定制家具工厂', '隆丰街道军屯村四组8586号', '', null, '1', '31.060436', '103.985896');
INSERT INTO `factory` VALUES ('944', '钧坤锋拓新能源商务车地板厂', '康安路229号', '', null, '1', '30.592829', '103.946448');
INSERT INTO `factory` VALUES ('945', '顾瑞全屋定制(工厂)', '聚尚美居家具厂东南侧170米', '', null, '1', '30.827572', '103.993712');
INSERT INTO `factory` VALUES ('946', '柯莱恩全屋定制工厂', '成都家具产业园列维士路358号', '', null, '1', '30.857837', '104.013198');
INSERT INTO `factory` VALUES ('947', '方师傅食品厂', '九尺镇宝马村16组74号', '', null, '1', '30.999676', '104.035274');
INSERT INTO `factory` VALUES ('948', '中铁十九局集团大件路改造项目钢筋加工厂', '月星路与西航港大道中三段交叉口东420米', '', null, '1', '30.556295', '103.982077');
INSERT INTO `factory` VALUES ('949', '琴悦钢琴批发厂', '铁佛路44号(簇桥地铁站C口步行370米)', '', null, '1', '30.610188', '103.990603');
INSERT INTO `factory` VALUES ('950', '郫县凯欣服装厂', '方碑街62-3栋附18号', '', null, '1', '30.766168', '104.017033');
INSERT INTO `factory` VALUES ('951', '龙桥陆陆勇制衣厂', '普华路一巷44号', '', null, '1', '30.814428', '104.030196');
INSERT INTO `factory` VALUES ('952', '张熠复合厂', '龙腾大道863号', '', null, '1', '30.814027', '104.034899');
INSERT INTO `factory` VALUES ('953', '成都德笙普集成吊顶厂', '太平园西部家居城5幢B4-5号', '', null, '1', '30.609625', '104.004890');
INSERT INTO `factory` VALUES ('954', '宴池酒厂', '同和路99-附59号', '', null, '1', '30.685097', '104.016576');
INSERT INTO `factory` VALUES ('955', '四川成都佳农宝菜加工厂', '清河村6组150号', '', null, '1', '30.878225', '104.048625');
INSERT INTO `factory` VALUES ('956', '爬山虎窗帘智能工厂', '斑竹园三山路公益10组61号4楼', '', null, '1', '30.827525', '104.049275');
INSERT INTO `factory` VALUES ('957', '四川庆宏电焊网厂', '小普路165号', '', null, '1', '30.805469', '104.049009');
INSERT INTO `factory` VALUES ('958', '成都超纯应用材料股份有限公司新建厂区', '华府大道四段19号', '', null, '1', '30.455883', '104.003368');
INSERT INTO `factory` VALUES ('959', '成都市骑龙净水厂(市第十二净水厂)', '祥华路2910号', '', null, '1', '30.537403', '104.021881');
INSERT INTO `factory` VALUES ('960', '成都钢豪加工厂', '', '', null, '1', '30.733230', '104.051024');
INSERT INTO `factory` VALUES ('961', '成都地奥九泓制造厂', '创业路辅路与九兴大道交叉口西南100米', '', null, '1', '30.618825', '104.041525');
INSERT INTO `factory` VALUES ('962', '成都众森源全屋定制家具厂', '斑竹园镇仁和村民大路978号', '', null, '1', '30.869625', '104.085875');
INSERT INTO `factory` VALUES ('963', '中铁八局成德线二工区钢筋厂', '北星大道一段6408正', '', null, '1', '30.801126', '104.075894');
INSERT INTO `factory` VALUES ('964', '都江堰市鹏辉塑料制品厂', '蒲阳镇双柏社区三组58号', '', null, '1', '31.028863', '103.708112');
INSERT INTO `factory` VALUES ('965', '明智酒厂', '府青路241号', '', null, '1', '30.580601', '103.632139');
INSERT INTO `factory` VALUES ('966', '四川金盆地(集团)有限公司新厂', '余塘村村委会南侧290米', '', null, '1', '30.665325', '103.664875');
INSERT INTO `factory` VALUES ('967', '乐家家具源头工厂', '团结路段32号', '', null, '1', '31.054825', '103.675325');
INSERT INTO `factory` VALUES ('968', '金柏莱家居工厂', '正科路169号', '', null, '1', '30.594341', '103.689851');
INSERT INTO `factory` VALUES ('969', '金盆地酒厂', '金盆地大道与晋康北路交叉口东40米', '', null, '1', '30.648512', '103.685239');
INSERT INTO `factory` VALUES ('970', '诺雅馨钢木家具厂', '画江大道三段与崇新路一段交叉口西南460米', '', null, '1', '30.543824', '103.761515');
INSERT INTO `factory` VALUES ('971', '成都超德创科技有限公司', '新园一路39号', '', null, '1', '30.265277', '103.647645');
INSERT INTO `factory` VALUES ('972', 'WEIO卫洛超级代工厂', '沙新路 368 号左转', '', null, '1', '30.515625', '103.741625');
INSERT INTO `factory` VALUES ('973', '成温邛扩容项目TJ1标钢筋加工厂', '新南路100号', '', null, '1', '30.712690', '103.824410');
INSERT INTO `factory` VALUES ('974', '成都嘎嘎辣卤工厂', '金马街道尚石路南段159号', '', null, '1', '30.660150', '103.775509');
INSERT INTO `factory` VALUES ('975', '德洛巴顿家具二分厂', '永兴街137号', '', null, '1', '30.845648', '103.817421');
INSERT INTO `factory` VALUES ('976', '四川馨三合食品有限公司', '丹景山镇', '', null, '1', '31.088298', '103.880860');
INSERT INTO `factory` VALUES ('977', '石材橱柜定制厂家', '濂溪村四组125号', '', null, '1', '30.837895', '103.891185');
INSERT INTO `factory` VALUES ('978', '一顶红伞蓬制品厂(源头工厂)', '安信路108-114', '', null, '1', '30.981168', '103.926585');
INSERT INTO `factory` VALUES ('979', '崇州市三江小金鱼皮鞋厂', '崇双大道三段1236号', '', null, '1', '30.576541', '103.811437');
INSERT INTO `factory` VALUES ('980', '彭州市名典家具厂', '天彭镇白马村5组1号', '', null, '1', '30.995675', '103.912925');
INSERT INTO `factory` VALUES ('981', '艾瑞杰铜铝不锈钢打包厂', '鹃兴路与郫彭路交叉口西北480米', '', null, '1', '30.825575', '103.894725');
INSERT INTO `factory` VALUES ('982', '成都政城通风设备有限公司(风管生产厂家)', '郫彭路蓬兴物流中转站内', '', null, '1', '30.849525', '103.909733');
INSERT INTO `factory` VALUES ('983', '成都市西园净水厂(市第十一净水厂)', '四川省成都市郫都区', '', null, '1', '30.748875', '103.909975');
INSERT INTO `factory` VALUES ('984', '成都鑫瑞龙机械制造有限公司', '彭镇工业园罗汉路南2段6号', '', null, '1', '30.585275', '103.880475');
INSERT INTO `factory` VALUES ('985', '鑫怡米粉厂', '九斗渠路', '', null, '1', '30.702679', '103.889182');
INSERT INTO `factory` VALUES ('986', '九洲昌隆高标准智能化农产品加工工厂', '涪陵路286号', '', null, '1', '30.612853', '103.891323');
INSERT INTO `factory` VALUES ('987', '索尔思光电(成都)有限公司-2号标准厂房', '科新路8号附5号', '', null, '1', '30.774657', '103.922418');
INSERT INTO `factory` VALUES ('988', '四川博亿包装有限公司', '现代工业港北片区港通北四路269号', '', null, '1', '30.810295', '103.928467');
INSERT INTO `factory` VALUES ('989', '碳晶板防撞板墙板金属雕花板厂', '红光街道港北二路569号1栋1层1号', '', null, '1', '30.808825', '103.939025');
INSERT INTO `factory` VALUES ('990', '广东华克思系统门窗厂', '九江镇九洋路4号铝合金门窗重型门折叠门阳光房雨棚葡萄架凉亭踢脚线平开门推拉门极窄门衣柜门极窄隔断系统门窗复古门窗', '', null, '1', '30.638001', '103.912847');
INSERT INTO `factory` VALUES ('991', '岷江水厂牧马山分厂', '云岭路52号', '', null, '1', '30.527646', '103.893869');
INSERT INTO `factory` VALUES ('992', '鲁班创美(双流工厂)', '成大路8号', '', null, '1', '30.634872', '103.913750');
INSERT INTO `factory` VALUES ('993', '千咏整装定制家具工厂', '隆丰街道军屯村四组8586号', '', null, '1', '31.060436', '103.985896');
INSERT INTO `factory` VALUES ('994', '钧坤锋拓新能源商务车地板厂', '康安路229号', '', null, '1', '30.592829', '103.946448');
INSERT INTO `factory` VALUES ('995', '顾瑞全屋定制(工厂)', '聚尚美居家具厂东南侧170米', '', null, '1', '30.827572', '103.993712');
INSERT INTO `factory` VALUES ('996', '方师傅食品厂', '九尺镇宝马村16组74号', '', null, '1', '30.999676', '104.035274');
INSERT INTO `factory` VALUES ('997', '中铁十九局集团大件路改造项目钢筋加工厂', '月星路与西航港大道中三段交叉口东420米', '', null, '1', '30.556295', '103.982077');
INSERT INTO `factory` VALUES ('998', '柯莱恩全屋定制工厂', '成都家具产业园列维士路358号', '', null, '1', '30.857837', '104.013198');
INSERT INTO `factory` VALUES ('999', '琴悦钢琴批发厂', '铁佛路44号(簇桥地铁站C口步行370米)', '', null, '1', '30.610188', '103.990603');
INSERT INTO `factory` VALUES ('1000', '郫县凯欣服装厂', '方碑街62-3栋附18号', '', null, '1', '30.766168', '104.017033');
INSERT INTO `factory` VALUES ('1001', '龙桥陆陆勇制衣厂', '普华路一巷44号', '', null, '1', '30.814428', '104.030196');
INSERT INTO `factory` VALUES ('1002', '张熠复合厂', '龙腾大道863号', '', null, '1', '30.814027', '104.034899');
INSERT INTO `factory` VALUES ('1003', '宴池酒厂', '同和路99-附59号', '', null, '1', '30.685097', '104.016576');
INSERT INTO `factory` VALUES ('1004', '成都德笙普集成吊顶厂', '太平园西部家居城5幢B4-5号', '', null, '1', '30.609625', '104.004890');
INSERT INTO `factory` VALUES ('1005', '四川成都佳农宝菜加工厂', '清河村6组150号', '', null, '1', '30.878225', '104.048625');
INSERT INTO `factory` VALUES ('1006', '爬山虎窗帘智能工厂', '斑竹园三山路公益10组61号4楼', '', null, '1', '30.827525', '104.049275');
INSERT INTO `factory` VALUES ('1007', '四川庆宏电焊网厂', '小普路165号', '', null, '1', '30.805469', '104.049009');
INSERT INTO `factory` VALUES ('1008', '成都超纯应用材料股份有限公司新建厂区', '华府大道四段19号', '', null, '1', '30.455883', '104.003368');
INSERT INTO `factory` VALUES ('1009', '成都市骑龙净水厂(市第十二净水厂)', '祥华路2910号', '', null, '1', '30.537403', '104.021881');
INSERT INTO `factory` VALUES ('1010', '成都钢豪加工厂', '', '', null, '1', '30.733230', '104.051024');
INSERT INTO `factory` VALUES ('1011', '成都地奥九泓制造厂', '创业路辅路与九兴大道交叉口西南100米', '', null, '1', '30.618825', '104.041525');
INSERT INTO `factory` VALUES ('1012', '成都众森源全屋定制家具厂', '斑竹园镇仁和村民大路978号', '', null, '1', '30.869625', '104.085875');
INSERT INTO `factory` VALUES ('1013', '中铁八局成德线二工区钢筋厂', '北星大道一段6408正', '', null, '1', '30.801126', '104.075894');
INSERT INTO `factory` VALUES ('1014', '明智酒厂', '府青路241号', '', null, '1', '30.580601', '103.632139');
INSERT INTO `factory` VALUES ('1015', '乐家家具源头工厂', '团结路段32号', '', null, '1', '31.054825', '103.675325');
INSERT INTO `factory` VALUES ('1016', '都江堰市鹏辉塑料制品厂', '蒲阳镇双柏社区三组58号', '', null, '1', '31.028863', '103.708112');
INSERT INTO `factory` VALUES ('1017', '四川金盆地(集团)有限公司新厂', '余塘村村委会南侧290米', '', null, '1', '30.665325', '103.664875');
INSERT INTO `factory` VALUES ('1018', '金盆地酒厂', '金盆地大道与晋康北路交叉口东40米', '', null, '1', '30.648512', '103.685239');
INSERT INTO `factory` VALUES ('1019', '金柏莱家居工厂', '正科路169号', '', null, '1', '30.594341', '103.689851');
INSERT INTO `factory` VALUES ('1020', 'WEIO卫洛超级代工厂', '沙新路 368 号左转', '', null, '1', '30.515625', '103.741625');
INSERT INTO `factory` VALUES ('1021', '成都超德创科技有限公司', '新园一路39号', '', null, '1', '30.265277', '103.647645');
INSERT INTO `factory` VALUES ('1022', '诺雅馨钢木家具厂', '画江大道三段与崇新路一段交叉口西南460米', '', null, '1', '30.543824', '103.761515');
INSERT INTO `factory` VALUES ('1023', '德洛巴顿家具二分厂', '永兴街137号', '', null, '1', '30.845648', '103.817421');
INSERT INTO `factory` VALUES ('1024', '成都嘎嘎辣卤工厂', '金马街道尚石路南段159号', '', null, '1', '30.660150', '103.775509');
INSERT INTO `factory` VALUES ('1025', '成温邛扩容项目TJ1标钢筋加工厂', '新南路100号', '', null, '1', '30.712690', '103.824410');
INSERT INTO `factory` VALUES ('1026', '石材橱柜定制厂家', '濂溪村四组125号', '', null, '1', '30.837895', '103.891185');
INSERT INTO `factory` VALUES ('1027', '彭州市名典家具厂', '天彭镇白马村5组1号', '', null, '1', '30.995675', '103.912925');
INSERT INTO `factory` VALUES ('1028', '崇州市三江小金鱼皮鞋厂', '崇双大道三段1236号', '', null, '1', '30.576541', '103.811437');
INSERT INTO `factory` VALUES ('1029', '艾瑞杰铜铝不锈钢打包厂', '鹃兴路与郫彭路交叉口西北480米', '', null, '1', '30.825575', '103.894725');
INSERT INTO `factory` VALUES ('1030', '四川馨三合食品有限公司', '丹景山镇', '', null, '1', '31.088298', '103.880860');
INSERT INTO `factory` VALUES ('1031', '一顶红伞蓬制品厂(源头工厂)', '安信路108-114', '', null, '1', '30.981168', '103.926585');
INSERT INTO `factory` VALUES ('1032', '成都政城通风设备有限公司(风管生产厂家)', '郫彭路蓬兴物流中转站内', '', null, '1', '30.849525', '103.909733');
INSERT INTO `factory` VALUES ('1033', '成都市西园净水厂(市第十一净水厂)', '四川省成都市郫都区', '', null, '1', '30.748875', '103.909975');
INSERT INTO `factory` VALUES ('1034', '鑫怡米粉厂', '九斗渠路', '', null, '1', '30.702679', '103.889182');
INSERT INTO `factory` VALUES ('1035', '九洲昌隆高标准智能化农产品加工工厂', '涪陵路286号', '', null, '1', '30.612853', '103.891323');
INSERT INTO `factory` VALUES ('1036', '成都鑫瑞龙机械制造有限公司', '彭镇工业园罗汉路南2段6号', '', null, '1', '30.585275', '103.880475');
INSERT INTO `factory` VALUES ('1037', '索尔思光电(成都)有限公司-2号标准厂房', '科新路8号附5号', '', null, '1', '30.774657', '103.922418');
INSERT INTO `factory` VALUES ('1038', '四川博亿包装有限公司', '现代工业港北片区港通北四路269号', '', null, '1', '30.810295', '103.928467');
INSERT INTO `factory` VALUES ('1039', '岷江水厂牧马山分厂', '云岭路52号', '', null, '1', '30.527646', '103.893869');
INSERT INTO `factory` VALUES ('1040', '广东华克思系统门窗厂', '九江镇九洋路4号铝合金门窗重型门折叠门阳光房雨棚葡萄架凉亭踢脚线平开门推拉门极窄门衣柜门极窄隔断系统门窗复古门窗', '', null, '1', '30.638001', '103.912847');
INSERT INTO `factory` VALUES ('1041', '碳晶板防撞板墙板金属雕花板厂', '红光街道港北二路569号1栋1层1号', '', null, '1', '30.808825', '103.939025');
INSERT INTO `factory` VALUES ('1042', '鲁班创美(双流工厂)', '成大路8号', '', null, '1', '30.634872', '103.913750');
INSERT INTO `factory` VALUES ('1043', '千咏整装定制家具工厂', '隆丰街道军屯村四组8586号', '', null, '1', '31.060436', '103.985896');
INSERT INTO `factory` VALUES ('1044', '钧坤锋拓新能源商务车地板厂', '康安路229号', '', null, '1', '30.592829', '103.946448');
INSERT INTO `factory` VALUES ('1045', '顾瑞全屋定制(工厂)', '聚尚美居家具厂东南侧170米', '', null, '1', '30.827572', '103.993712');
INSERT INTO `factory` VALUES ('1046', '方师傅食品厂', '九尺镇宝马村16组74号', '', null, '1', '30.999676', '104.035274');
INSERT INTO `factory` VALUES ('1047', '柯莱恩全屋定制工厂', '成都家具产业园列维士路358号', '', null, '1', '30.857837', '104.013198');
INSERT INTO `factory` VALUES ('1048', '中铁十九局集团大件路改造项目钢筋加工厂', '月星路与西航港大道中三段交叉口东420米', '', null, '1', '30.556295', '103.982077');
INSERT INTO `factory` VALUES ('1049', '琴悦钢琴批发厂', '铁佛路44号(簇桥地铁站C口步行370米)', '', null, '1', '30.610188', '103.990603');
INSERT INTO `factory` VALUES ('1050', '郫县凯欣服装厂', '方碑街62-3栋附18号', '', null, '1', '30.766168', '104.017033');
INSERT INTO `factory` VALUES ('1051', '龙桥陆陆勇制衣厂', '普华路一巷44号', '', null, '1', '30.814428', '104.030196');
INSERT INTO `factory` VALUES ('1052', '宴池酒厂', '同和路99-附59号', '', null, '1', '30.685097', '104.016576');
INSERT INTO `factory` VALUES ('1053', '成都德笙普集成吊顶厂', '太平园西部家居城5幢B4-5号', '', null, '1', '30.609625', '104.004890');
INSERT INTO `factory` VALUES ('1054', '张熠复合厂', '龙腾大道863号', '', null, '1', '30.814027', '104.034899');
INSERT INTO `factory` VALUES ('1055', '四川成都佳农宝菜加工厂', '清河村6组150号', '', null, '1', '30.878225', '104.048625');
INSERT INTO `factory` VALUES ('1056', '四川庆宏电焊网厂', '小普路165号', '', null, '1', '30.805469', '104.049009');
INSERT INTO `factory` VALUES ('1057', '爬山虎窗帘智能工厂', '斑竹园三山路公益10组61号4楼', '', null, '1', '30.827525', '104.049275');
INSERT INTO `factory` VALUES ('1058', '成都市骑龙净水厂(市第十二净水厂)', '祥华路2910号', '', null, '1', '30.537403', '104.021881');
INSERT INTO `factory` VALUES ('1059', '成都超纯应用材料股份有限公司新建厂区', '华府大道四段19号', '', null, '1', '30.455883', '104.003368');
INSERT INTO `factory` VALUES ('1060', '成都钢豪加工厂', '', '', null, '1', '30.733230', '104.051024');
INSERT INTO `factory` VALUES ('1061', '成都地奥九泓制造厂', '创业路辅路与九兴大道交叉口西南100米', '', null, '1', '30.618825', '104.041525');
INSERT INTO `factory` VALUES ('1062', '中铁八局成德线二工区钢筋厂', '北星大道一段6408正', '', null, '1', '30.801126', '104.075894');
INSERT INTO `factory` VALUES ('1063', '成都众森源全屋定制家具厂', '斑竹园镇仁和村民大路978号', '', null, '1', '30.869625', '104.085875');
INSERT INTO `factory` VALUES ('1064', '都江堰市鹏辉塑料制品厂', '蒲阳镇双柏社区三组58号', '', null, '1', '31.028863', '103.708112');
INSERT INTO `factory` VALUES ('1065', '乐家家具源头工厂', '团结路段32号', '', null, '1', '31.054825', '103.675325');
INSERT INTO `factory` VALUES ('1066', '明智酒厂', '府青路241号', '', null, '1', '30.580601', '103.632139');
INSERT INTO `factory` VALUES ('1067', '四川金盆地(集团)有限公司新厂', '余塘村村委会南侧290米', '', null, '1', '30.665325', '103.664875');
INSERT INTO `factory` VALUES ('1068', '金盆地酒厂', '金盆地大道与晋康北路交叉口东40米', '', null, '1', '30.648512', '103.685239');
INSERT INTO `factory` VALUES ('1069', '金柏莱家居工厂', '正科路169号', '', null, '1', '30.594341', '103.689851');
INSERT INTO `factory` VALUES ('1070', 'WEIO卫洛超级代工厂', '沙新路 368 号左转', '', null, '1', '30.515625', '103.741625');
INSERT INTO `factory` VALUES ('1071', '成都超德创科技有限公司', '新园一路39号', '', null, '1', '30.265277', '103.647645');
INSERT INTO `factory` VALUES ('1072', '成都嘎嘎辣卤工厂', '金马街道尚石路南段159号', '', null, '1', '30.660150', '103.775509');
INSERT INTO `factory` VALUES ('1073', '诺雅馨钢木家具厂', '画江大道三段与崇新路一段交叉口西南460米', '', null, '1', '30.543824', '103.761515');
INSERT INTO `factory` VALUES ('1074', '德洛巴顿家具二分厂', '永兴街137号', '', null, '1', '30.845648', '103.817421');
INSERT INTO `factory` VALUES ('1075', '崇州市三江小金鱼皮鞋厂', '崇双大道三段1236号', '', null, '1', '30.576541', '103.811437');
INSERT INTO `factory` VALUES ('1076', '成温邛扩容项目TJ1标钢筋加工厂', '新南路100号', '', null, '1', '30.712690', '103.824410');
INSERT INTO `factory` VALUES ('1077', '四川馨三合食品有限公司', '丹景山镇', '', null, '1', '31.088298', '103.880860');
INSERT INTO `factory` VALUES ('1078', '彭州市名典家具厂', '天彭镇白马村5组1号', '', null, '1', '30.995675', '103.912925');
INSERT INTO `factory` VALUES ('1079', '石材橱柜定制厂家', '濂溪村四组125号', '', null, '1', '30.837895', '103.891185');
INSERT INTO `factory` VALUES ('1080', '艾瑞杰铜铝不锈钢打包厂', '鹃兴路与郫彭路交叉口西北480米', '', null, '1', '30.825575', '103.894725');
INSERT INTO `factory` VALUES ('1081', '一顶红伞蓬制品厂(源头工厂)', '安信路108-114', '', null, '1', '30.981168', '103.926585');
INSERT INTO `factory` VALUES ('1082', '成都政城通风设备有限公司(风管生产厂家)', '郫彭路蓬兴物流中转站内', '', null, '1', '30.849525', '103.909733');
INSERT INTO `factory` VALUES ('1083', '鑫怡米粉厂', '九斗渠路', '', null, '1', '30.702679', '103.889182');
INSERT INTO `factory` VALUES ('1084', '成都鑫瑞龙机械制造有限公司', '彭镇工业园罗汉路南2段6号', '', null, '1', '30.585275', '103.880475');
INSERT INTO `factory` VALUES ('1085', '成都市西园净水厂(市第十一净水厂)', '四川省成都市郫都区', '', null, '1', '30.748875', '103.909975');
INSERT INTO `factory` VALUES ('1086', '九洲昌隆高标准智能化农产品加工工厂', '涪陵路286号', '', null, '1', '30.612853', '103.891323');
INSERT INTO `factory` VALUES ('1087', '索尔思光电(成都)有限公司-2号标准厂房', '科新路8号附5号', '', null, '1', '30.774657', '103.922418');
INSERT INTO `factory` VALUES ('1088', '四川博亿包装有限公司', '现代工业港北片区港通北四路269号', '', null, '1', '30.810295', '103.928467');
INSERT INTO `factory` VALUES ('1089', '岷江水厂牧马山分厂', '云岭路52号', '', null, '1', '30.527646', '103.893869');
INSERT INTO `factory` VALUES ('1090', '广东华克思系统门窗厂', '九江镇九洋路4号铝合金门窗重型门折叠门阳光房雨棚葡萄架凉亭踢脚线平开门推拉门极窄门衣柜门极窄隔断系统门窗复古门窗', '', null, '1', '30.638001', '103.912847');
INSERT INTO `factory` VALUES ('1091', '碳晶板防撞板墙板金属雕花板厂', '红光街道港北二路569号1栋1层1号', '', null, '1', '30.808825', '103.939025');
INSERT INTO `factory` VALUES ('1092', '鲁班创美(双流工厂)', '成大路8号', '', null, '1', '30.634872', '103.913750');
INSERT INTO `factory` VALUES ('1093', '千咏整装定制家具工厂', '隆丰街道军屯村四组8586号', '', null, '1', '31.060436', '103.985896');
INSERT INTO `factory` VALUES ('1094', '钧坤锋拓新能源商务车地板厂', '康安路229号', '', null, '1', '30.592829', '103.946448');
INSERT INTO `factory` VALUES ('1095', '顾瑞全屋定制(工厂)', '聚尚美居家具厂东南侧170米', '', null, '1', '30.827572', '103.993712');
INSERT INTO `factory` VALUES ('1096', '柯莱恩全屋定制工厂', '成都家具产业园列维士路358号', '', null, '1', '30.857837', '104.013198');
INSERT INTO `factory` VALUES ('1097', '方师傅食品厂', '九尺镇宝马村16组74号', '', null, '1', '30.999676', '104.035274');
INSERT INTO `factory` VALUES ('1098', '中铁十九局集团大件路改造项目钢筋加工厂', '月星路与西航港大道中三段交叉口东420米', '', null, '1', '30.556295', '103.982077');
INSERT INTO `factory` VALUES ('1099', '琴悦钢琴批发厂', '铁佛路44号(簇桥地铁站C口步行370米)', '', null, '1', '30.610188', '103.990603');
INSERT INTO `factory` VALUES ('1100', '郫县凯欣服装厂', '方碑街62-3栋附18号', '', null, '1', '30.766168', '104.017033');
INSERT INTO `factory` VALUES ('1101', '龙桥陆陆勇制衣厂', '普华路一巷44号', '', null, '1', '30.814428', '104.030196');
INSERT INTO `factory` VALUES ('1102', '张熠复合厂', '龙腾大道863号', '', null, '1', '30.814027', '104.034899');
INSERT INTO `factory` VALUES ('1103', '成都德笙普集成吊顶厂', '太平园西部家居城5幢B4-5号', '', null, '1', '30.609625', '104.004890');
INSERT INTO `factory` VALUES ('1104', '宴池酒厂', '同和路99-附59号', '', null, '1', '30.685097', '104.016576');
INSERT INTO `factory` VALUES ('1105', '四川成都佳农宝菜加工厂', '清河村6组150号', '', null, '1', '30.878225', '104.048625');
INSERT INTO `factory` VALUES ('1106', '爬山虎窗帘智能工厂', '斑竹园三山路公益10组61号4楼', '', null, '1', '30.827525', '104.049275');
INSERT INTO `factory` VALUES ('1107', '四川庆宏电焊网厂', '小普路165号', '', null, '1', '30.805469', '104.049009');
INSERT INTO `factory` VALUES ('1108', '成都超纯应用材料股份有限公司新建厂区', '华府大道四段19号', '', null, '1', '30.455883', '104.003368');
INSERT INTO `factory` VALUES ('1109', '成都市骑龙净水厂(市第十二净水厂)', '祥华路2910号', '', null, '1', '30.537403', '104.021881');
INSERT INTO `factory` VALUES ('1110', '成都钢豪加工厂', '', '', null, '1', '30.733230', '104.051024');
INSERT INTO `factory` VALUES ('1111', '成都地奥九泓制造厂', '创业路辅路与九兴大道交叉口西南100米', '', null, '1', '30.618825', '104.041525');
INSERT INTO `factory` VALUES ('1112', '成都众森源全屋定制家具厂', '斑竹园镇仁和村民大路978号', '', null, '1', '30.869625', '104.085875');
INSERT INTO `factory` VALUES ('1113', '中铁八局成德线二工区钢筋厂', '北星大道一段6408正', '', null, '1', '30.801126', '104.075894');
INSERT INTO `factory` VALUES ('1114', '乐家家具源头工厂', '团结路段32号', '', null, '1', '31.054825', '103.675325');
INSERT INTO `factory` VALUES ('1115', '都江堰市鹏辉塑料制品厂', '蒲阳镇双柏社区三组58号', '', null, '1', '31.028863', '103.708112');
INSERT INTO `factory` VALUES ('1116', '明智酒厂', '府青路241号', '', null, '1', '30.580601', '103.632139');
INSERT INTO `factory` VALUES ('1117', '四川金盆地(集团)有限公司新厂', '余塘村村委会南侧290米', '', null, '1', '30.665325', '103.664875');
INSERT INTO `factory` VALUES ('1118', '金盆地酒厂', '金盆地大道与晋康北路交叉口东40米', '', null, '1', '30.648512', '103.685239');
INSERT INTO `factory` VALUES ('1119', '金柏莱家居工厂', '正科路169号', '', null, '1', '30.594341', '103.689851');
INSERT INTO `factory` VALUES ('1120', '成都超德创科技有限公司', '新园一路39号', '', null, '1', '30.265277', '103.647645');
INSERT INTO `factory` VALUES ('1121', 'WEIO卫洛超级代工厂', '沙新路 368 号左转', '', null, '1', '30.515625', '103.741625');
INSERT INTO `factory` VALUES ('1122', '成都嘎嘎辣卤工厂', '金马街道尚石路南段159号', '', null, '1', '30.660150', '103.775509');
INSERT INTO `factory` VALUES ('1123', '诺雅馨钢木家具厂', '画江大道三段与崇新路一段交叉口西南460米', '', null, '1', '30.543824', '103.761515');
INSERT INTO `factory` VALUES ('1124', '成温邛扩容项目TJ1标钢筋加工厂', '新南路100号', '', null, '1', '30.712690', '103.824410');
INSERT INTO `factory` VALUES ('1125', '德洛巴顿家具二分厂', '永兴街137号', '', null, '1', '30.845648', '103.817421');
INSERT INTO `factory` VALUES ('1126', '四川馨三合食品有限公司', '丹景山镇', '', null, '1', '31.088298', '103.880860');
INSERT INTO `factory` VALUES ('1127', '彭州市名典家具厂', '天彭镇白马村5组1号', '', null, '1', '30.995675', '103.912925');
INSERT INTO `factory` VALUES ('1128', '崇州市三江小金鱼皮鞋厂', '崇双大道三段1236号', '', null, '1', '30.576541', '103.811437');
INSERT INTO `factory` VALUES ('1129', '石材橱柜定制厂家', '濂溪村四组125号', '', null, '1', '30.837895', '103.891185');
INSERT INTO `factory` VALUES ('1130', '艾瑞杰铜铝不锈钢打包厂', '鹃兴路与郫彭路交叉口西北480米', '', null, '1', '30.825575', '103.894725');
INSERT INTO `factory` VALUES ('1131', '一顶红伞蓬制品厂(源头工厂)', '安信路108-114', '', null, '1', '30.981168', '103.926585');
INSERT INTO `factory` VALUES ('1132', '鑫怡米粉厂', '九斗渠路', '', null, '1', '30.702679', '103.889182');
INSERT INTO `factory` VALUES ('1133', '成都鑫瑞龙机械制造有限公司', '彭镇工业园罗汉路南2段6号', '', null, '1', '30.585275', '103.880475');
INSERT INTO `factory` VALUES ('1134', '成都政城通风设备有限公司(风管生产厂家)', '郫彭路蓬兴物流中转站内', '', null, '1', '30.849525', '103.909733');
INSERT INTO `factory` VALUES ('1135', '索尔思光电(成都)有限公司-2号标准厂房', '科新路8号附5号', '', null, '1', '30.774657', '103.922418');
INSERT INTO `factory` VALUES ('1136', '九洲昌隆高标准智能化农产品加工工厂', '涪陵路286号', '', null, '1', '30.612853', '103.891323');
INSERT INTO `factory` VALUES ('1137', '成都市西园净水厂(市第十一净水厂)', '四川省成都市郫都区', '', null, '1', '30.748875', '103.909975');
INSERT INTO `factory` VALUES ('1138', '四川博亿包装有限公司', '现代工业港北片区港通北四路269号', '', null, '1', '30.810295', '103.928467');
INSERT INTO `factory` VALUES ('1139', '岷江水厂牧马山分厂', '云岭路52号', '', null, '1', '30.527646', '103.893869');
INSERT INTO `factory` VALUES ('1140', '碳晶板防撞板墙板金属雕花板厂', '红光街道港北二路569号1栋1层1号', '', null, '1', '30.808825', '103.939025');
INSERT INTO `factory` VALUES ('1141', '广东华克思系统门窗厂', '九江镇九洋路4号铝合金门窗重型门折叠门阳光房雨棚葡萄架凉亭踢脚线平开门推拉门极窄门衣柜门极窄隔断系统门窗复古门窗', '', null, '1', '30.638001', '103.912847');
INSERT INTO `factory` VALUES ('1142', '鲁班创美(双流工厂)', '成大路8号', '', null, '1', '30.634872', '103.913750');
INSERT INTO `factory` VALUES ('1143', '千咏整装定制家具工厂', '隆丰街道军屯村四组8586号', '', null, '1', '31.060436', '103.985896');
INSERT INTO `factory` VALUES ('1144', '顾瑞全屋定制(工厂)', '聚尚美居家具厂东南侧170米', '', null, '1', '30.827572', '103.993712');
INSERT INTO `factory` VALUES ('1145', '柯莱恩全屋定制工厂', '成都家具产业园列维士路358号', '', null, '1', '30.857837', '104.013198');
INSERT INTO `factory` VALUES ('1146', '方师傅食品厂', '九尺镇宝马村16组74号', '', null, '1', '30.999676', '104.035274');
INSERT INTO `factory` VALUES ('1147', '钧坤锋拓新能源商务车地板厂', '康安路229号', '', null, '1', '30.592829', '103.946448');
INSERT INTO `factory` VALUES ('1148', '中铁十九局集团大件路改造项目钢筋加工厂', '月星路与西航港大道中三段交叉口东420米', '', null, '1', '30.556295', '103.982077');
INSERT INTO `factory` VALUES ('1149', '琴悦钢琴批发厂', '铁佛路44号(簇桥地铁站C口步行370米)', '', null, '1', '30.610188', '103.990603');
INSERT INTO `factory` VALUES ('1150', '张熠复合厂', '龙腾大道863号', '', null, '1', '30.814027', '104.034899');
INSERT INTO `factory` VALUES ('1151', '龙桥陆陆勇制衣厂', '普华路一巷44号', '', null, '1', '30.814428', '104.030196');
INSERT INTO `factory` VALUES ('1152', '郫县凯欣服装厂', '方碑街62-3栋附18号', '', null, '1', '30.766168', '104.017033');
INSERT INTO `factory` VALUES ('1153', '成都德笙普集成吊顶厂', '太平园西部家居城5幢B4-5号', '', null, '1', '30.609625', '104.004890');
INSERT INTO `factory` VALUES ('1154', '宴池酒厂', '同和路99-附59号', '', null, '1', '30.685097', '104.016576');
INSERT INTO `factory` VALUES ('1155', '四川成都佳农宝菜加工厂', '清河村6组150号', '', null, '1', '30.878225', '104.048625');
INSERT INTO `factory` VALUES ('1156', '爬山虎窗帘智能工厂', '斑竹园三山路公益10组61号4楼', '', null, '1', '30.827525', '104.049275');
INSERT INTO `factory` VALUES ('1157', '四川庆宏电焊网厂', '小普路165号', '', null, '1', '30.805469', '104.049009');
INSERT INTO `factory` VALUES ('1158', '成都地奥九泓制造厂', '创业路辅路与九兴大道交叉口西南100米', '', null, '1', '30.618825', '104.041525');
INSERT INTO `factory` VALUES ('1159', '成都市骑龙净水厂(市第十二净水厂)', '祥华路2910号', '', null, '1', '30.537403', '104.021881');
INSERT INTO `factory` VALUES ('1160', '成都超纯应用材料股份有限公司新建厂区', '华府大道四段19号', '', null, '1', '30.455883', '104.003368');
INSERT INTO `factory` VALUES ('1161', '成都钢豪加工厂', '', '', null, '1', '30.733230', '104.051024');
INSERT INTO `factory` VALUES ('1162', '中铁八局成德线二工区钢筋厂', '北星大道一段6408正', '', null, '1', '30.801126', '104.075894');
INSERT INTO `factory` VALUES ('1163', '成都众森源全屋定制家具厂', '斑竹园镇仁和村民大路978号', '', null, '1', '30.869625', '104.085875');
INSERT INTO `factory` VALUES ('1164', '乐家家具源头工厂', '团结路段32号', '', null, '1', '31.054825', '103.675325');
INSERT INTO `factory` VALUES ('1165', '明智酒厂', '府青路241号', '', null, '1', '30.580601', '103.632139');
INSERT INTO `factory` VALUES ('1166', '都江堰市鹏辉塑料制品厂', '蒲阳镇双柏社区三组58号', '', null, '1', '31.028863', '103.708112');
INSERT INTO `factory` VALUES ('1167', '金盆地酒厂', '金盆地大道与晋康北路交叉口东40米', '', null, '1', '30.648512', '103.685239');
INSERT INTO `factory` VALUES ('1168', '四川金盆地(集团)有限公司新厂', '余塘村村委会南侧290米', '', null, '1', '30.665325', '103.664875');
INSERT INTO `factory` VALUES ('1169', '金柏莱家居工厂', '正科路169号', '', null, '1', '30.594341', '103.689851');
INSERT INTO `factory` VALUES ('1170', '成都超德创科技有限公司', '新园一路39号', '', null, '1', '30.265277', '103.647645');
INSERT INTO `factory` VALUES ('1171', '成都嘎嘎辣卤工厂', '金马街道尚石路南段159号', '', null, '1', '30.660150', '103.775509');
INSERT INTO `factory` VALUES ('1172', 'WEIO卫洛超级代工厂', '沙新路 368 号左转', '', null, '1', '30.515625', '103.741625');
INSERT INTO `factory` VALUES ('1173', '诺雅馨钢木家具厂', '画江大道三段与崇新路一段交叉口西南460米', '', null, '1', '30.543824', '103.761515');
INSERT INTO `factory` VALUES ('1174', '乐家家具源头工厂', '团结路段32号', '', null, '1', '31.054825', '103.675325');
INSERT INTO `factory` VALUES ('1175', '明智酒厂', '府青路241号', '', null, '1', '30.580601', '103.632139');
INSERT INTO `factory` VALUES ('1176', '都江堰市鹏辉塑料制品厂', '蒲阳镇双柏社区三组58号', '', null, '1', '31.028863', '103.708112');
INSERT INTO `factory` VALUES ('1177', '金柏莱家居工厂', '正科路169号', '', null, '1', '30.594341', '103.689851');
INSERT INTO `factory` VALUES ('1178', '金盆地酒厂', '金盆地大道与晋康北路交叉口东40米', '', null, '1', '30.648512', '103.685239');
INSERT INTO `factory` VALUES ('1179', '四川金盆地(集团)有限公司新厂', '余塘村村委会南侧290米', '', null, '1', '30.665325', '103.664875');
INSERT INTO `factory` VALUES ('1180', '成都超德创科技有限公司', '新园一路39号', '', null, '1', '30.265277', '103.647645');
INSERT INTO `factory` VALUES ('1181', '诺雅馨钢木家具厂', '画江大道三段与崇新路一段交叉口西南460米', '', null, '1', '30.543824', '103.761515');
INSERT INTO `factory` VALUES ('1182', '成都嘎嘎辣卤工厂', '金马街道尚石路南段159号', '', null, '1', '30.660150', '103.775509');
INSERT INTO `factory` VALUES ('1183', 'WEIO卫洛超级代工厂', '沙新路 368 号左转', '', null, '1', '30.515625', '103.741625');
INSERT INTO `factory` VALUES ('1184', '乐家家具源头工厂', '团结路段32号', '', null, '1', '31.054825', '103.675325');
INSERT INTO `factory` VALUES ('1185', '明智酒厂', '府青路241号', '', null, '1', '30.580601', '103.632139');
INSERT INTO `factory` VALUES ('1186', '四川金盆地(集团)有限公司新厂', '余塘村村委会南侧290米', '', null, '1', '30.665325', '103.664875');
INSERT INTO `factory` VALUES ('1187', '都江堰市鹏辉塑料制品厂', '蒲阳镇双柏社区三组58号', '', null, '1', '31.028863', '103.708112');
INSERT INTO `factory` VALUES ('1188', '金盆地酒厂', '金盆地大道与晋康北路交叉口东40米', '', null, '1', '30.648512', '103.685239');
INSERT INTO `factory` VALUES ('1189', '金柏莱家居工厂', '正科路169号', '', null, '1', '30.594341', '103.689851');
INSERT INTO `factory` VALUES ('1190', '成都超德创科技有限公司', '新园一路39号', '', null, '1', '30.265277', '103.647645');
INSERT INTO `factory` VALUES ('1191', '成都嘎嘎辣卤工厂', '金马街道尚石路南段159号', '', null, '1', '30.660150', '103.775509');
INSERT INTO `factory` VALUES ('1192', 'WEIO卫洛超级代工厂', '沙新路 368 号左转', '', null, '1', '30.515625', '103.741625');
INSERT INTO `factory` VALUES ('1193', '诺雅馨钢木家具厂', '画江大道三段与崇新路一段交叉口西南460米', '', null, '1', '30.543824', '103.761515');

-- ----------------------------
-- Table structure for goods
-- ----------------------------
DROP TABLE IF EXISTS `goods`;
CREATE TABLE `goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '货物ID',
  `goodsName` varchar(50) NOT NULL COMMENT '货物名称',
  `vol` decimal(10,2) DEFAULT NULL COMMENT '体积',
  `weight` decimal(10,2) DEFAULT NULL COMMENT '重量',
  `owner` varchar(50) DEFAULT NULL COMMENT '货主',
  `packType` varchar(10) DEFAULT '散' COMMENT '包装类型：袋、箱、瓶、散',
  `factort_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `货物_ibfk_1` (`factort_id`),
  CONSTRAINT `goods_ibfk_1` FOREIGN KEY (`factort_id`) REFERENCES `factory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of goods
-- ----------------------------

-- ----------------------------
-- Table structure for mission
-- ----------------------------
DROP TABLE IF EXISTS `mission`;
CREATE TABLE `mission` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `missionNo` varchar(30) NOT NULL COMMENT '订单编号',
  `car_id` int(11) DEFAULT NULL COMMENT '关联车辆ID',
  `goods_id` int(11) DEFAULT NULL COMMENT '关联货物ID',
  `goods_type` varchar(50) DEFAULT NULL COMMENT '货物类型',
  `quantity` int(11) DEFAULT 1 COMMENT '数量',
  `totalWeight` decimal(10,2) DEFAULT NULL COMMENT '总重量(kg)',
  `totalVol` decimal(10,2) DEFAULT NULL COMMENT '总体积(m³)',
  `distance_km` double DEFAULT 0 COMMENT '起点到终点距离(km)',
  `total_minutes` int(11) DEFAULT 0 COMMENT '任务总耗时(分钟)',
  `elapsed_minutes` int(11) DEFAULT 0 COMMENT '已耗时(分钟)',
  `status` varchar(20) DEFAULT '待处理' COMMENT '状态：待接单、接单中、装货中、运输中、卸货中、已完成',
  `createTime` datetime DEFAULT current_timestamp() COMMENT '创建时间',
  `factory_id` int(11) DEFAULT NULL COMMENT '起点工厂',
  `dest_factory_id` int(11) DEFAULT NULL COMMENT '终点工厂',
  `route_id` int(11) DEFAULT NULL,
  `need_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `orderNo` (`missionNo`),
  KEY `订单_ibfk_3` (`factory_id`),
  KEY `order_ibfk_2` (`goods_id`),
  KEY `order_ibfk_4` (`route_id`),
  KEY `order_ibfk_5` (`need_id`),
  KEY `order2` (`car_id`),
  CONSTRAINT `order2` FOREIGN KEY (`car_id`) REFERENCES `vehicle` (`id`),
  CONSTRAINT `order_ibfk_5` FOREIGN KEY (`need_id`) REFERENCES `need` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of mission
-- ----------------------------

-- ----------------------------
-- Table structure for need
-- ----------------------------
DROP TABLE IF EXISTS `need`;
CREATE TABLE `need` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `needContent` varchar(255) DEFAULT '',
  `factory_id` int(11) DEFAULT NULL,
  `isDeleted` tinyint(10) DEFAULT 0,
  `assigned` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of need
-- ----------------------------
INSERT INTO `need` VALUES ('1', '木头', '1', '1', '0');
INSERT INTO `need` VALUES ('2', '木头', '3', '1', '0');
INSERT INTO `need` VALUES ('3', '木头', '1', '0', '0');

-- ----------------------------
-- Table structure for poi
-- ----------------------------
DROP TABLE IF EXISTS `poi`;
CREATE TABLE `poi` (
  `id` varchar(100) NOT NULL,
  `POI_type` varchar(255) DEFAULT '',
  `POI_location` varchar(255) DEFAULT '',
  `POI_function` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of poi
-- ----------------------------

-- ----------------------------
-- Table structure for route
-- ----------------------------
DROP TABLE IF EXISTS `route`;
CREATE TABLE `route` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '路线ID',
  `startPointName` varchar(100) DEFAULT NULL COMMENT '起点POI名称',
  `endPointName` varchar(100) DEFAULT NULL COMMENT '终点POI名称',
  `startPoint` varchar(100) DEFAULT NULL COMMENT '起点坐标/位置标识',
  `endPoint` varchar(100) DEFAULT NULL COMMENT '终点坐标/位置标识',
  `roadType` varchar(20) DEFAULT NULL COMMENT '道路类型：高速、国道、省道、其他',
  `distance` decimal(10,2) DEFAULT NULL COMMENT '距离(km)',
  `keyPoint` text DEFAULT NULL COMMENT '中间关键点，可存多个点描述/坐标，逗号分隔或JSON',
  `estimatedTime` int(11) DEFAULT NULL COMMENT '预计时长(分钟)，可选',
  `status` varchar(10) DEFAULT '可用' COMMENT '状态：可用/拥堵/封闭',
  `createTime` datetime DEFAULT current_timestamp() COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `route_ibfk_1` (`startPoint`),
  KEY `route_ibfk_2` (`endPoint`),
  CONSTRAINT `route_ibfk_1` FOREIGN KEY (`startPoint`) REFERENCES `poi` (`id`),
  CONSTRAINT `route_ibfk_2` FOREIGN KEY (`endPoint`) REFERENCES `poi` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of route
-- ----------------------------

-- ----------------------------
-- Table structure for vehicle
-- ----------------------------
DROP TABLE IF EXISTS `vehicle`;
CREATE TABLE `vehicle` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `BandName` varchar(50) NOT NULL COMMENT '品牌名称',
  `licenseNumber` varchar(20) NOT NULL COMMENT '车牌号',
  `TypeCode` varchar(20) DEFAULT NULL COMMENT '类型编码',
  `CurrentLatitude` double DEFAULT NULL,
  `CurrentLongitude` double DEFAULT NULL COMMENT '当前位置',
  `CurrentAction` int(100) DEFAULT NULL COMMENT '当前动作/状态',
  `isDeleted` tinyint(1) DEFAULT 0,
  `remaining_time` int(11) DEFAULT 0 COMMENT '当前状态剩余时间(分钟)',
  `distance_to_pickup` double DEFAULT 0 COMMENT '到取货点距离(km)',
  `transport_distance` double DEFAULT 0 COMMENT '运输距离(km)',
  PRIMARY KEY (`id`),
  KEY `1` (`CurrentAction`),
  CONSTRAINT `1` FOREIGN KEY (`CurrentAction`) REFERENCES `action` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of vehicle
-- ----------------------------
INSERT INTO `vehicle` VALUES ('12', '东风', '川A·00011', '货车', '30.56', '104.05', '1', '0', '0', '0', '0');
INSERT INTO `vehicle` VALUES ('13', '东风', '川A·00012', '货车', '30.57', '104.06', '1', '0', '0', '0', '0');
