from datetime import datetime

from django.contrib import admin
from django import forms
from daterange_filter.filter import DateRangeFilter
from django.db.models import Count

from network.models import *


class AddressInline(admin.TabularInline):
	model = Address
	
	readonly_fields = ('latitude', 'longitude', 'country_code', 'get_flag', 'country', 'city', 'type', 'ip', 'port')

	fieldsets = [
		('', {'fields': ('get_flag', 'country', 'city', 'type', 'ip', 'port', 'latitude', 'longitude', )}),
	]	

	extra = 0

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

class NodeAdmin(admin.ModelAdmin):
	readonly_fields = ('alias', 'nodeid', 'get_geo', 'last_timestamp', 'color')

	list_display = ('get_geo', 'alias', 'nodeid', 'last_timestamp')
	list_display_links = ('get_geo', 'alias', 'nodeid',)
	list_filter = (('last_timestamp', DateRangeFilter),)

	search_fields = ('nodeid', 'alias',)

	inlines = [AddressInline,]

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

class ChannelAdmin(admin.ModelAdmin):
	readonly_fields = ('source_node', 'destination_node', 'short_channel_id', 'active', 'public', 'flags', 'fee_per_millionth', 'base_fee_millisatoshi', 'delay', 'last_update')

	list_display = ('short_channel_id', 'active', 'public', 'flags', 'fee_per_millionth', 'base_fee_millisatoshi', 'delay', 'last_update')
	list_filter = (('last_update', DateRangeFilter), 'active', 'public')

	search_fields = ('short_channel_id', 'source_node', 'destination_node', )

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False
		

admin.site.register(Node, NodeAdmin)
admin.site.register(Channel, ChannelAdmin)
