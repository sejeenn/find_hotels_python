import random
data = {
    'id': '39176263', 'name': 'Capitol Hotel', 'address': 'Narimanov Str.17, Baku, AZ1069',
    'coordinates': {'__typename': 'Coordinates', 'latitude': 40.404908, 'longitude': 49.84422},
    'images': [
        'https://images.trvl-media.com/lodging/40000000/39180000/39176300/39176263/ce0ca9f7.jpg?impolicy=resizecrop&rw=500&ra=fit',
        'https://images.trvl-media.com/lodging/40000000/39180000/39176300/39176263/53674ad7.jpg?impolicy=resizecrop&rw=500&ra=fit',
        'https://images.trvl-media.com/lodging/40000000/39180000/39176300/39176263/4d846f42.jpg?impolicy=resizecrop&rw=500&ra=fit',
        'https://images.trvl-media.com/lodging/40000000/39180000/39176300/39176263/2cef5842.jpg?impolicy=resizecrop&rw=500&ra=fit',
        'https://images.trvl-media.com/lodging/40000000/39180000/39176300/39176263/eba15ce2.jpg?impolicy=resizecrop&rw=500&ra=fit',
        'https://images.trvl-media.com/lodging/40000000/39180000/39176300/39176263/81b05423.jpg?impolicy=resizecrop&rw=500&ra=fit',
        'https://images.trvl-media.com/lodging/40000000/39180000/39176300/39176263/35dc826b.jpg?impolicy=resizecrop&rw=500&ra=fit',
        'https://images.trvl-media.com/lodging/40000000/39180000/39176300/39176263/6155b83a.jpg?impolicy=resizecrop&rw=500&ra=fit',
        'https://images.trvl-media.com/lodging/40000000/39180000/39176300/39176263/2b387c15.jpg?impolicy=resizecrop&rw=500&ra=fit',
        'https://images.trvl-media.com/lodging/40000000/39180000/39176300/39176263/98a0baae.jpg?impolicy=resizecrop&rw=500&ra=fit'
    ]
}

test = data['images'][random.randint(0, len(data['images']) - 1)]
print(len(data['images']))
print(test)
