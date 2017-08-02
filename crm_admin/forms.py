# coding: utf-8
__author__ = "HanQian"

from  django.forms import ModelForm


def __new__(cls, *args, **kwargs):
    for field_name in cls.base_fields:
        field = cls.base_fields[field_name]
        attr_dic = {"class": "form-control" }
        field.widget.attrs.update(attr_dic)
    return ModelForm.__new__(cls)

def create_modelform(model_class):
    """动态生成modelform"""
    class Meta:
        model = model_class
        fields = "__all__"

    modelform = type("DynamicModelForm",
                     (ModelForm,),
                     {"Meta": Meta, "__new__": __new__},
                     )
    return  modelform
 #form_obj = dynamic_modelform(instance=model_obj)