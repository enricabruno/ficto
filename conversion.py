#Import libraries
import rdflib
import csv
import re
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, OWL, SKOS

# Create the graph
g = rdflib.Graph()

# Namespaces
ficto = Namespace("https://example.org/ficto/")
lrmoo = Namespace("http://iflastandards.info/ns/lrm/lrmoo/")
frbroo = Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/")
rdau = Namespace("http://rdaregistry.info/Elements/u/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
dul = Namespace("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")
prov = Namespace("http://www.w3.org/ns/prov#")
cito = Namespace("http://purl.org/spar/cito/") 

# Associate prefix to the graph
g.bind("ficto", ficto)
g.bind("lrmoo", lrmoo)
g.bind("frbroo", frbroo)
g.bind("rdau", rdau)
g.bind("crm", crm)
g.bind("dul", dul)
g.bind("prov", prov)
g.bind("cito", cito)

# CSV WORK CREATION
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - WorkCreation.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"WorkCreation/"+str(row.get(list(row.keys())[0]))), RDF.type, lrmoo.F27))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"WorkCreation/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # Data time=value is a digit
                    elif value.isdigit():
                        obj = Literal(int(value), datatype=XSD.gYear)
                    # Data language=value is a language code
                    elif value == "ita" or value == "fra":
                        obj = Literal(value, datatype=XSD.language)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # Value corresponding to column
                    elif key=="rdau:P60447" or key=="rdau:P60447" or key=="rdau:P60385":
                        obj = URIRef(ficto+"Agent/"+str(value))
                    # Otherwise, value=URI
                    elif key=="lrmoo:R16":
                        obj = URIRef(ficto+"Work/"+str(value))
                    elif key=="lrmoo:R3" or key=="lrmoo:R17":
                        obj = URIRef(ficto+"Expression/"+str(value))
                    elif key=="crm:P94":
                        obj = URIRef(ficto+"Narrative/"+str(value))
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# CSV WORK
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - Work.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"Work/"+str(row.get(list(row.keys())[0]))), RDF.type, lrmoo.F1))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"Work/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # Data time=value is a digit
                    elif value.isdigit():
                        obj = Literal(int(value), datatype=XSD.gYear)
                    # Data language=value is a language code
                    elif value == "ita" or value == "fra":
                        obj = Literal(value, datatype=XSD.language)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # Value corresponding to column
                    elif key=="rdau:P60447" or key=="rdau:P60447" or key=="rdau:P60385":
                        obj = URIRef(ficto+"Agent/"+str(value))
                    # Otherwise, value=URI
                    elif key=="lrmoo:R16":
                        obj = URIRef(ficto+"Work/"+str(value))
                    elif key=="lrmoo:R3" or key=="lrmoo:R17":
                        obj = URIRef(ficto+"Expression/"+str(value))
                    elif key=="crm:P94":
                        obj = URIRef(ficto+"Narrative/"+str(value))
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# CSV EXPRESSION CREATION
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - ExpressionCreation.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"ExpressionCreation/"+str(row.get(list(row.keys())[0]))), RDF.type, lrmoo.F28))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"ExpressionCreation/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # Data time=value is a digit
                    elif value.isdigit():
                        obj = Literal(int(value), datatype=XSD.gYear)
                    # Data language=value is a language code
                    elif value == "ita" or value == "fra":
                        obj = Literal(value, datatype=XSD.language)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # Value corresponding to column
                    elif key=="rdau:P60447" or key=="rdau:P60447" or key=="rdau:P60385":
                        obj = URIRef(ficto+"Agent/"+str(value))
                    # obj=work
                    elif key=="lrmoo:R16":
                        obj = URIRef(ficto+"Work/"+str(value))
                    # obj=expr
                    elif key=="lrmoo:R3" or key=="lrmoo:R17":
                        obj = URIRef(ficto+"Expression/"+str(value))
                    # obj= narr
                    elif key=="crm:P94":
                        obj = URIRef(ficto+"Narrative/"+str(value))
                    #obj=type
                    elif key=="crm:P2":
                        obj = URIRef(ficto+"Type/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))
                    g.add((subj, predicate, obj))

# CSV EXPRESSION
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - Expression.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"Expression/"+str(row.get(list(row.keys())[0]))), RDF.type, lrmoo.F2))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"Expression/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # Data time=value is a digit
                    elif value.isdigit():
                        obj = Literal(int(value), datatype=XSD.gYear)
                    # Data language=value is a language code
                    elif value == "ita" or value == "fra":
                        obj = Literal(value, datatype=XSD.language)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # Value corresponding to column
                    elif key=="rdau:P60447" or key=="rdau:P60447" or key=="rdau:P60385":
                        obj = URIRef(ficto+"Agent/"+str(value))
                    # Otherwise, value=URI
                    elif key=="lrmoo:R16":
                        obj = URIRef(ficto+"Work/"+str(value))
                    elif key=="lrmooo:R3" or key=="lrmoo:R17":
                        obj = URIRef(ficto+"Expression/"+str(value))
                    elif key=="crm:P94":
                        obj = URIRef(ficto+"Narrative/"+str(value))
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# CSV AUTHORITY COLLECT AGENT
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - AuthorityCollectAgent.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"CollectiveAgent/"+str(row.get(list(row.keys())[0]))), RDF.type, lrmoo.F55))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"CollectiveAgent/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# CSV AUTHORITY AGENT
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - AuthorityAgent.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"Agent/"+str(row.get(list(row.keys())[0]))), RDF.type, crm.E39))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"Agent/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# CSV GENRE
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - LiteraryGenre.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"LiteraryGenre/"+str(row.get(list(row.keys())[0]))), RDF.type, ficto.LiteraryGenre))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"LiteraryGenre/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# CSV NARRATIVE
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - Narrative.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"Narrative/"+str(row.get(list(row.keys())[0]))), RDF.type, dul.Narrative))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"Narrative/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # When obj=narrseg
                    elif key=="crm:P46":
                        obj = URIRef(ficto+"NarrativeSegment/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# CSV CHARACTER
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - Character.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"Character/"+str(row.get(list(row.keys())[0]))), RDF.type, frbroo.F38))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"Character/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # When obj=role
                    elif key=="ficto:narrativeRole":
                        obj = URIRef(ficto+"Role/"+str(value))
                    # When obj=character
                    elif key=="ficto:isInspiredBy":
                        obj = URIRef(ficto+"Character/"+str(value))
                    # When obj=agent
                    elif key=="frbroo:R57":
                        obj = URIRef(ficto+"Agent/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# CSV NARRATOR
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - Narrator.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"Narrator/"+str(row.get(list(row.keys())[0]))), RDF.type, ficto.Narrator))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"Narrator/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # When obj=narrative position
                    elif key=="ficto:hasNarrativePosition":
                        obj = URIRef(ficto+"NarrativePosition/"+str(value))
                    # When obj=narrative level
                    elif key=="ficto:hasNarrativeLevel":
                        obj = URIRef(ficto+"NarrativeLevel/"+str(value))
                    # When obj=focalization
                    elif key=="ficto:hasPointOfView":
                        obj = URIRef(ficto+"Focalization/"+str(value))
                    # When obj=charac
                    elif key=="owl:sameAs":
                        obj = URIRef(ficto+"Character/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# CSV CONCEPT
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - Concept.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"Concept/"+str(row.get(list(row.keys())[0]))), RDF.type, SKOS.Concept))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"Concept/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # Value corresponding to column
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# NARRATIVE SEGMENT
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - NarrativeSegment.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-Z]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+"Narrative/"+str(row.get(list(row.keys())[0]))), RDF.type, ficto.NarrativeSegment))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+"Narrative/"+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # When obj is a character
                    elif key=="ficto:involves":
                        obj = URIRef(ficto+"Character/"+str(value))
                    # When obj is a narrator
                    elif key=="ficto:hasNarrativeInstance":
                        obj = URIRef(ficto+"Narrator/"+str(value))
                    # When obj is a form of speech
                    elif key=="ficto:hasFormOfSpeech":
                        obj = URIRef(ficto+"FormOfSpeech/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# ANAGR STATUS
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - AnagraphicalStatus.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-ZÉ]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+str(row.get(list(row.keys())[0]))), RDF.type, ficto.AnagraphicalStatus))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # When obj=concept
                    elif key=="skos:related":
                        obj = URIRef(ficto+"Concept/"+str(value))
                    # When obj=genre
                    elif key=="ficto:linkedTo":
                        obj = URIRef(ficto+"LiteraryGenre/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# CHAR/PS
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - CharacterAndPsychology.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-ZÉ]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+str(row.get(list(row.keys())[0]))), RDF.type, ficto.CharacterAndPsychology))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # When obj=concept
                    elif key=="skos:related":
                        obj = URIRef(ficto+"Concept/"+str(value))
                    # When obj=genre
                    elif key=="ficto:linkedTo":
                        obj = URIRef(ficto+"LiteraryGenre/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# PRAXIS
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - Praxis.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-ZÉ]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+str(row.get(list(row.keys())[0]))), RDF.type, ficto.Praxis))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # When obj=concept
                    elif key=="skos:related":
                        obj = URIRef(ficto+"Concept/"+str(value))
                    # When obj=genre
                    elif key=="ficto:linkedTo":
                        obj = URIRef(ficto+"LiteraryGenre/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# MODALITY
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - Modality.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-ZÉ]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+str(row.get(list(row.keys())[0]))), RDF.type, ficto.Modality))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # When obj=concept
                    elif key=="skos:related":
                        obj = URIRef(ficto+"Concept/"+str(value))
                    # When obj=genre
                    elif key=="ficto:linkedTo":
                        obj = URIRef(ficto+"LiteraryGenre/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# AXIOLOGY
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - Axiology.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-ZÉ]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+str(row.get(list(row.keys())[0]))), RDF.type, ficto.Axiology))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # When obj=concept
                    elif key=="skos:related":
                        obj = URIRef(ficto+"Concept/"+str(value))
                    # When obj=genre
                    elif key=="ficto:linkedTo":
                        obj = URIRef(ficto+"LiteraryGenre/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# SYMBOLS
with open("/Users/enrica/Documents/GitHub/ficto/csv-files/NEW-dataset-MITE - Symbols.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Iteration through each row
    for row in csv_reader:
        #Iterate through each key of the row
        for key in row.keys():
            # Retrieves the value of the current key and removes whitespaces
            value = row.get(key).strip()

            # Reg ex for capital letters and URIs
            capital_letter_regex = re.compile(r'^[A-ZÉ]')
            http_regex = re.compile(r'\bhttps?://\S+')
            uncinate_regex = re.compile(r'^«[^»]*»')

            # Add a triple that associates the first column's value in the row with the type of entity
            g.add((URIRef(ficto+str(row.get(list(row.keys())[0]))), RDF.type, ficto.Symbols))

            # Skip the first key
            if key != list (row.keys())[0]:

                # Check if the value is empy
                if value:

                    # Subject
                    subj = URIRef(ficto+str(row.get(list(row.keys())[0])))

                    # Split the predicate in prefix and suffix
                    column_split = str(key).split(":")
                    prefix = column_split[0]
                    suffix = column_split[1]

                    namespaces = {"ficto":"https://example.org/ficto/",
                    "lrmoo":"http://iflastandards.info/ns/lrm/lrmoo/",
                    "frbroo":"http://iflastandards.info/ns/fr/frbr/frbroo/",
                    "rdau":"http://rdaregistry.info/Elements/u/",
                    "rdfs":"http://www.w3.org/TR/rdf11-schema/",
                    "crm":"http://www.cidoc-crm.org/cidoc-crm/",
                    "dul":"http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "prov":"http://www.w3.org/ns/prov#",
                    "owl" : "http://www.w3.org/TR/owl-ref/",
                    "rdfs" : "http://www.w3.org/TR/rdf11-schema/",
                    "dul" : "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
                    "cito" : "http://purl.org/spar/cito/",
                    "skos" : "http://www.w3.org/2004/02/skos/core#"}

                    # Check if the prefix is in the Dict and create the predicate URI
                    predicate = ''
                    if prefix in namespaces:
                        base_uri = namespaces[prefix]
                        predicate = URIRef(base_uri+suffix)
                        if prefix == "owl":
                            predicate = OWL.sameAs
                        if prefix == "rdfs":
                            predicate = RDFS.label

                    # Determine the object
                    obj = ''
                    # String=value with capital letters
                    if capital_letter_regex.match(value) or uncinate_regex.match(value):
                        obj = Literal(value, datatype=XSD.string)
                    # String URI=value is a URI
                    elif http_regex.match(value):
                        obj = Literal(value, datatype=XSD.anyURI)
                    # When obj=concept
                    elif key=="skos:related":
                        obj = URIRef(ficto+"Concept/"+str(value))
                    # When obj=genre
                    elif key=="ficto:linkedTo":
                        obj = URIRef(ficto+"LiteraryGenre/"+str(value))
                    # Otherwise, value=URI
                    else:
                        obj = URIRef(ficto+str(value))

                    g.add((subj, predicate, obj))

# Serialize the graph to a TTL file
g.serialize(destination="kbficto.ttl", format="ttl")

# Optionally, print the triples in the graph for verification
#for s, p, o in g.triples((None, None, None)):
    #print(s, p, o)