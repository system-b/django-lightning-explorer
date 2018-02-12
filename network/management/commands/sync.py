from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from network.models import *
from backend import settings
from backend.lib.pylightning import LightningRpc

import geoip2.database


reader_city = geoip2.database.Reader(settings.GEO_CITY_PATH)


class Command(BaseCommand):
	help = ''

	def handle(self, *args, **options):
		rpc = LightningRpc(settings.LIGHTNING_RPC)

		node_list = rpc.listnodes()['nodes']
		
		for _ in node_list:
			try:
				node = Node.objects.get(nodeid=_['nodeid'])
			except:
				node = Node()
				node.nodeid = _['nodeid']
			
			node.alias = _.get('alias', '--')
			node.color = _.get('color', 'ffffff')
			node.last_timestamp = datetime.fromtimestamp(_.get('last_timestamp', 0))
			node.save()
			
			for _ in _.get('addresses', []):
				try:
					address_type = 0 if _['type'] == 'ipv4' else 1
					
					try:
						address = Address.objects.get(node=node, ip=_['address'], port=_['port'], type=address_type)
					except:
						address = Address()
						address.node = node
						address.type = address_type
						address.ip = _['address']
						address.port = _['port']
					
					if reader_city.city(_['address']):
						address.country_code = reader_city.city(_['address']).country.iso_code
						address.country = reader_city.city(_['address']).country.name
						address.city = reader_city.city(_['address']).city.name
						address.longitude = reader_city.city(_['address']).location.longitude
						address.latitude = reader_city.city(_['address']).location.latitude
					
					address.save()
				except Exception as e:
					# print(e)
					pass
	
		channel_list = rpc.listchannels()['channels']
		
		for _ in channel_list:
			try:
				try:
					channel = Channel.objects.get(short_channel_id=_['short_channel_id'])
				except:
					channel = Channel()
					channel.source_node = Node.objects.get(nodeid=_['source'])
					channel.destination_node = Node.objects.get(nodeid=_['destination'])
					channel.short_channel_id = _['short_channel_id']
				
				channel.active = _.get('active', 0)
				channel.public = _.get('public', 0)
				channel.delay = _.get('delay', 0)
				channel.fee_per_millionth = _.get('fee_per_millionth', 0)
				channel.base_fee_millisatoshi = _.get('base_fee_millisatoshi', 0)
				channel.last_update = datetime.fromtimestamp(_.get('last_update', 0))
				channel.flags = _.get('flags', 0)
				channel.save()
			except Exception as e:
				# print(e)
				pass
				
			
