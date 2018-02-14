import humanize

from django.db import models
from django.utils.safestring import mark_safe

from backend import settings


class Node(models.Model):
	nodeid = models.CharField(max_length=255, unique=True)
	
	alias = models.CharField(max_length=255, null=True, blank=True)
	color = models.CharField(max_length=6, null=True, blank=True)
	
	last_timestamp = models.DateTimeField(null=True, blank=True)

	def get_naturaltime(self):
		return humanize.naturaltime(self.last_timestamp)

	def get_name(self):
		return self.alias

	def get_url(self):
		return '/node/%s' % self.nodeid

	def get_channel_count(self):
		return Channel.objects.filter(source_node=self).count()

	def get_channel_list(self):
		return Channel.objects.filter(source_node=self).order_by('-last_update')

	def get_address_list(self):
		return Address.objects.filter(node=self)

	def get_address_count(self):
		return Address.objects.filter(node=self).count()

	def __unicode__(self):
		return self.get_name()

	def __str__(self):
		return self.get_name()

	def get_geo(self):
		geo_str = ''
		for _ in Address.objects.filter(node=self)[:5]:
			geo_str += '<img class="flag" width="20" alt="%s" title="%s" src="https://lipis.github.io/flag-icon-css/flags/4x3/%s.svg">' % (_.country, _.country, _.country_code.lower())
		if Address.objects.filter(node=self).count() >= 5:
			geo_str = geo_str[:-2]+'...'
		return mark_safe(geo_str)
	get_geo.short_description = 'GEO'
	get_geo.admin_order_field = 'id'


class Address(models.Model):
	node = models.ForeignKey(Node, related_name="address_node", null=True, blank=True, on_delete=models.PROTECT)
	
	type = models.IntegerField(choices=((0, 'ipv4'), (1, 'ipv6')), default=0)
	ip = models.CharField(max_length=255, null=True, blank=True)
	port = models.IntegerField(default=9735, null=True, blank=True)
	
	country_code = models.CharField(max_length=2, null=True, blank=True)
	
	country = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	
	latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

	def get_flag(self):
		if self.country_code:
			return mark_safe('<img class="flag" width="20" alt="%s" title="%s" src="https://lipis.github.io/flag-icon-css/flags/4x3/%s.svg">' % (self.country, self.country, self.country_code.lower()))
		else:
			return '--'
	get_flag.short_description = 'GEO'
	get_flag.admin_order_field = 'id'


	def get_name(self):
		return self.get_type_display()+self.ip+':'+str(self.port)

	def __unicode__(self):
		return self.get_name()

	def __str__(self):
		return self.get_name()
		
class Channel(models.Model):
	source_node = models.ForeignKey(Node, related_name="channel_source_node", null=True, blank=True, on_delete=models.PROTECT)
	destination_node = models.ForeignKey(Node, related_name="channel_source_destination", null=True, blank=True, on_delete=models.PROTECT)
	
	short_channel_id = models.CharField(max_length=20, null=True, blank=True)
	
	last_update = models.DateTimeField(null=True, blank=True)
	
	active = models.BooleanField(default=True,)
	public = models.BooleanField(default=True,)
	
	flags = models.IntegerField(default=0, null=True, blank=True)
	fee_per_millionth = models.IntegerField(default=0, null=True, blank=True)
	base_fee_millisatoshi = models.IntegerField(default=0, null=True, blank=True)
	delay = models.IntegerField(default=0, null=True, blank=True)
	
	def get_naturaltime(self):
		return humanize.naturaltime(self.last_update)
	
	def get_name(self):
		return str(self.id)

	def __unicode__(self):
		return self.get_name()

	def __str__(self):
		return self.get_name()
	
	
