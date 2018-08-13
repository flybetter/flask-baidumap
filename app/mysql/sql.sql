CREATE TABLE lianjia_json
				(
				id int PRIMARY KEY AUTO_INCREMENT,
				name varchar(255) COMMENT '小区名称',
				json text COMMENT '小区',
				children_json text COMMENT '关联小区'
				)