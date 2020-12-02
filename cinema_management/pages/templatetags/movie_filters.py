from django import template
import json
register = template.Library()

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    return dict_data.get(key)

@register.filter('get_sum_price_seats')
def get_sum_price_seats(seats):
    price_sum = 0
    for seat in seats:
        price_sum += seat['price']
    return price_sum

@register.filter('get_sum_price_combos')
def get_sum_price_combos(combos):
    price_sum = 0
    for combo in combos:
        price_sum += combo['price']
    return price_sum

@register.filter('to_json')
def to_json(obj):
    return json.dumps(obj)