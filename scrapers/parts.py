urls = [
        "https://t-auto.bg/",
        "https://maxcar.bg/",
        "https://topcar.bg/"
        ]


# engine oil urls
base_url = "https://maxcar.bg/avtomobilni-masla/"
viscosity = "10w40"
quantity = "5"
price_asc = "product.price.asc"
price_desc = "product.price.desc"
engine_oil_url = f"{base_url}viskozitet-{viscosity}/litri-{quantity}_litra?order={price_desc}"


# brake pads urls
base_url_pads = "https://maxcar.bg/avtochasti/diskovi-spirachki.html" # opens a form to be filled with:
# brand example <option value="5">AUDI</option> (.upper())
brand_select_element = '//*[@id="search_blocktdm_querym"]'

# model example (<option value="6418" nmn="A4 (8K2, B8)">A4 (8K2, B8) - (2007 - 2018) </option>)
model_select_element = '//*[@id="search_blocktdm_querymodel"]'

# engine selector example <option value="117078">2.0 TFSI (140 kW-190 к.С.) - бензин - CVKB, DBPA, DEMA</option>
engine_select_element = '//*[@id="search_blocktdm_querymtype"]'
