# Pin specifires constants

# :var SUPPORTED_DATA_TYPES: To specify supported data types list  用于指定支持的数据类型列表。
# :var CONSTRAINT: To specify type constraint key  用于指定类型约束的键。
# :var STRUCT_CONSTRAINT: To specify struct constraint key  用于指定结构约束的键。
# :var ENABLED_OPTIONS: To enable options  用于启用选项。
# :var DISABLED_OPTIONS: To disable options  用于禁用选项。
# :var INPUT_WIDGET_VARIANT: To specify widget variant string  用于指定输入小部件的变种字符串。
# :var DESCRIPTION: To specify description for pin, which will be used as tooltip   用于指定引脚的描述，该描述将用作工具提示。
# :var VALUE_LIST: Specific for string pin. If specified, combo box will be created   针对字符串引脚具体。如果指定了这个常量，将创建一个下拉框（combo box）。
# :var VALUE_RANGE: Specific for ints and floats. If specified, slider will be created instead of value box   针对整数和浮点数。如果指定了这个常量，将创建一个滑块（slider）而不是数值框（value box）。
# :var DRAGGER_STEPS: To specify custom value dragger steps   用于指定自定义值拖动器的步骤。




#下面为一个函数模板的示例
import math
import random

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)

from PyFlow.Core.Common import *


class IntLib(FunctionLibraryBase):
    """doc string for IntLib"""
    def __init__(self, packageName):
        super(IntLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.STRUCT_CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}), meta={NodeMeta.CATEGORY: 'tempLib', NodeMeta.KEYWORDS: ['get']})
    def appendTo(obj=('AnyPin', None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.STRUCT_CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                element=("AnyPin", None, {PinSpecifires.CONSTRAINT: "1"}),
                result=(REF, ('BoolPin', False))):
        """Calls ``obj.append(element)``. And returns object. If failed - object is unchanged"""
        try:
            obj.append(element)
            result(True)
            return obj
        except:
            result(False)
            return obj