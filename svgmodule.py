from lxml import etree
import lxml.etree as et

def RemoveImage(svgPath):
	try:
		tree = etree.parse(open(svgPath))
	except:
		print('failed to open svgPath')
		pass

	root = tree.getroot()

	try:
		target = root.xpath("/svg:svg/svg:image", namespaces={"svg": "http://www.w3.org/2000/svg"})
	except:
		print('ERROR: svgPath image element did not found')

	try:	
		target[0].getparent().remove(target[0])
	except:
		pass
	'''
	for element in root.iter("*"):
		print(element)
	'''
	try:
		with open(svgPath, 'wb') as f:
		    f.write(etree.tostring(tree))
	except:
		print('ERROR: failed to save modified svg file')
