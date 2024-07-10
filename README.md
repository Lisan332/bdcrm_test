

重构公司的一shi山代码，针对三方同学的一些接口做一些自动化测试

预发布环境1

http://crm.prod.baidu.com/

预发布环境2

http://crm.prod.baidu.com/



外网测试暂时用的百度账号权限(内网暂时用passpord，后期内网需要迁移到uuap平台)，环境需要登录百度账号https://passport.baidu.com/，



以用户管理为例进行的测试用例

1. **创建用户**：
   - 测试创建用户的功能。
   - 验证创建后的数据是否正确。
2. **获取用户信息**：
   - 测试获取用户信息的功能。
   - 验证获取到的用户数据是否正确。
3. **更新用户信息**：
   - 测试更新用户信息的功能。
   - 验证更新后的数据是否正确。
4. **列出所有用户**：
   - 测试列出所有用户的功能。
   - 验证返回的用户列表是否包含至少一个用户。
5. **删除用户**：
   - 测试删除用户的功能。
   - 验证用户是否被成功删除。

### 运行测试：

1. 确保你有 `requests` 和 `unittest` 模块。你可以通过 `pip install requests` 安装 `requests` 模块。
2. 将代码保存到一个 Python 文件中（例如 `test_user_management.py`）。
3. 运行测试：`python test_user_management.py`。

### 预期输出：

#### 设置：

- 创建一个新的用户，用于测试各种操作。

#### 日志格式：

```
2024-6-24 10:02:01 - INFO - Created user: {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'password123', 'role': 'user'}
2024-6-24 10:02:01 - INFO - Retrieved user data: {'id': '1', 'username': 'testuser', 'email': 'testuser@example.com', 'role': 'user'}
2024-6-24 10:02:01 - INFO - Updated user with ID 1 to: {'username': 'updateduser', 'email': 'updateduser@example.com', 'role': 'admin'}
2024-6-24 10:02:02 - INFO - Verified updated user data: {'id': '1', 'username': 'updateduser', 'email': 'updateduser@example.com', 'role': 'admin'}
2024-6-24 10:02:02 - INFO - Listed users: [{'id': '1', 'username': 'testuser', 'email': 'testuser@example.com', 'role': 'user'}]
2024-6-24 10:02:02 - INFO - Deleted user with ID: 1
2024-6-24 10:02:02 - INFO - Verified user with ID 1 no longer exists
```

.
