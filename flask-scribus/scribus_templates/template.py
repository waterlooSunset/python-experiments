# Import sys, os, json
import sys, os, json

# get job info id which is passed by the --python-arg flag
jobInfoID = sys.argv[2]

# open job json that contains information we use to fill in our template
jsonObj = None

with open(os.path.join('jobs', jobInfoID + '.json')) as json_file:
    jsonObj = json.load(json_file)

# open doc
scribus.openDoc(os.path.join('scribus_templates', jsonObj['template'] + '.sla'))

# change title
scribus.setText(jsonObj['title'], "title")
scribus.setTextAlignment(1, "title")
scribus.setFontSize(24, "title")

# change image
scribus.loadImage(os.path.join('jobs', jsonObj['image']), 'image_1')
scribus.setScaleImageToFrame(scaletoframe=1, proportional=0, name='image_1')

# change text
scribus.setText(jsonObj['text'], "text")

# save as pdf
pdf = scribus.PDFfile()
pdf.file = os.path.join('pdf', jobInfoID + '.pdf')
pdf.save()

# save as img
img = scribus.ImageExport()
img.type = 'jpg'
img.scale = 50
img.quality = 80
img.name = os.path.join('pdf', jobInfoID + '.jpg')
img.save()

# delete jobs info json and images
os.remove(os.path.join('jobs', jobInfoID + '.json'))
os.remove(os.path.join('jobs', jsonObj['image']))
