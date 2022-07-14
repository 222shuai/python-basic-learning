import unittest
import blood_pressure


class TestDifferenceCalculate(unittest.TestCase):
    def test_difference_calculate(self):  # 1.测试:difference_calculate(差值计算)函数
        # 第一组输入：以31-35岁的男性为例,其对应正常参考值为117,76。因此预期返回值为2,3
        age, sex_ = '31-35', 'man'  # 待测函数所需输入值
        input_value = blood_pressure.pressure_dict[age][sex_]  # 待测函数输入值input_value
        result = tuple(blood_pressure.difference_calculate(input_value, sex_))  # 结果转为元组形式方便测试
        self.assertEqual((2, 3), result)  # 断言测试结果
        # 第二组输入：以31-35岁的女性为例,其对应正常参考值为114,74。因此预期返回值为4,4
        age, sex_ = '31-35', 'woman'  # 待测函数所需输入值
        input_value = blood_pressure.pressure_dict[age][sex_]  # 待测函数输入值input_value
        result = tuple(blood_pressure.difference_calculate(input_value, sex_))  # 结果转为元组形式方便测试
        self.assertEqual((4, 4), result)  # 断言测试结果
        # 第三组输入：以36-40岁的男性为例,其对应正常参考值为120,80。因此预期返回值为5,7
        age, sex_ = '36-40', 'man'  # 待测函数所需输入值
        input_value = blood_pressure.pressure_dict[age][sex_]  # 待测函数输入值input_value
        result = tuple(blood_pressure.difference_calculate(input_value, sex_))  # 结果转为元组形式方便测试
        self.assertEqual((5, 7), result)  # 断言测试结果


class TestBloodPressure(unittest.TestCase):
    def test_blood_pressure(self):  # 2.测试:blood_pressure(血压测试)函数,均以16-20岁男性为例
        age, sex_ = '16-20', 'man'  # 待测函数的后两个输入(16-20岁的男性)
        # 第一组输入(高血压):
        value1, value2 = 145, 55  # 待测函数的前两个输入(收缩压和舒张压)
        result = blood_pressure.blood_pressure(value1, value2, age, sex_)  # 接收返回结果
        self.assertEqual('高血压！', result)  # 断言高血压输入测试结果
        # 第二组输入(正常高值血压):
        value1, value2 = 130, 55  # 待测函数的前两个输入(收缩压和舒张压)
        result = blood_pressure.blood_pressure(value1, value2, age, sex_)  # 接收返回结果
        self.assertEqual('正常高值血压！', result)  # 断言正常高值血压输入测试结果
        # 第三组输入(正常血压):
        value1, value2 = 110, 55  # 待测函数的前两个输入(收缩压和舒张压)
        result = blood_pressure.blood_pressure(value1, value2, age, sex_)  # 接收返回结果
        self.assertEqual('正常血压！', result)  # 断言正常血压输入测试结果
        # 第四组输入(低血压):
        value1, value2 = 85, 55  # 待测函数的前两个输入(收缩压和舒张压)
        result = blood_pressure.blood_pressure(value1, value2, age, sex_)  # 接收返回结果
        self.assertEqual('低血压！', result)  # 断言低血压输入测试结果


class TestRunMain(unittest.TestCase):
    def test_run_main(self):  # 3.测试run_main()程序主函数
        age, sex_ = '16-20', 'man'  # 待测函数的后两个输入(16-20岁的男性)
        # 第一组输入(整型检验):
        value1, value2 = 55.5, 32.4  # 待测函数的前两个输入(收缩压和舒张压)
        result = blood_pressure.run_main(value1, value2, age, sex_)  # 接收返回结果
        self.assertEqual('请输入整数！', result)  # 断言非整数输入测试结果
        # 第二组输入(非负性检验):
        value1, value2 = 85, -55  # 待测函数的前两个输入(收缩压和舒张压)
        result = blood_pressure.run_main(value1, value2, age, sex_)  # 接收返回结果
        self.assertEqual('请输入正整数！', result)  # 断言负数输入测试结果
        # 第三组输入(收缩压大于舒张压检验):
        value1, value2 = 50, 85  # 待测函数的前两个输入(收缩压和舒张压)
        result = blood_pressure.run_main(value1, value2, age, sex_)  # 接收返回结果
        self.assertEqual('输入异常！', result)  # 断言收缩压小于舒张压输入测试结果
        # 第四组输入(正常输入):
        value1, value2 = 110, 55  # 待测函数的前两个输入(收缩压和舒张压)
        result = blood_pressure.run_main(value1, value2, age, sex_)  # 接收返回结果
        self.assertEqual('正常血压！', result)  # 断言正常血压输入测试结果


if __name__ == '__main__':
    unittest.main()
