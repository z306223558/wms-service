# coding=utf-8

import json

from django.forms import Widget
from django.utils.safestring import mark_safe


class JsonEditorWidget(Widget):
    """
    在django admin 后台中使用jsoneditor处理JSONField
    TODO：有待改进, 这里使用 % 格式化，使用 format 会抛出 KeyError 异常
    """

    html_template = """
        <div id='%(name)s_editor_holder' style='padding-left:170px;'></div>
        <textarea name="%(name)s" id="id_%(name)s" value="%(value)s"></textarea>
        <style type="text/css">
            #%(name)s_editor_holder h3 {
                font-size: 14px;
                padding: 0;
            }
            #id_%(name)s {
                display:none;
            }
        </style>
        <script type="text/javascript">
            var element = document.getElementById('%(name)s_editor_holder');
            var json_value_%(name)s = %(value)s;
            var schema = {
              "title": "在库物料信息",
              "type": "object",
              "options": {
                "collapsed": true
              },
              "properties": {
                "materials": {
                  "type": "array",
                  "title": "物料列表",
                  "uniqueItems": false,
                  "format": "table",
                  "items": {
                    "type": "object",
                    "title": "物料",
                    "properties": {
                      "name": {
                        "type": "string",
                        "title": "物料名称"
                      },
                      "id": {
                        "type": "integer",
                        "title": "物料ID"
                      },
                      "count": {
                        "type": "integer",
                        "title": "在库库存数量"
                      },
                      "expired_date": {
                        "type": "string",
                        "format": "datetime",
                        "title": "过期时间"
                      },
                      "inbound_date": {
                        "type": "string",
                        "format": "datetime",
                        "title": "入库时间"
                      }
                    }
                  }
                }
              }
            }
            var %(name)s_editor = new JSONEditor(element, {
                schema: schema,
                iconlib: 'fontawesome4',
                remove_button_labels: true,
                theme: 'bootstrap2',
                compact: true,
                object_layout: 'table',
                disable_properties: true,
                disable_edit_json: true,
            });
            
            if(JSON.stringify(json_value_%(name)s) !== '{}'){
                %(name)s_editor.setValue(json_value_%(name)s);     
            }
            
            %(name)s_editor.disable();
            
            %(name)s_editor.on("change",  function() {
                var textarea = document.getElementById('id_%(name)s');
                var json_changed =  JSON.stringify(%(name)s_editor.getValue());
                console.log(json_changed + '...................')
                textarea.value = json_changed;   
            });
            
        </script>
        """

    def __init__(self, attrs=None):
        super(JsonEditorWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if isinstance(value, str):
            value = json.loads(value)

        result = self.html_template % {'name': name, 'value': json.dumps(value), }
        return mark_safe(result)
