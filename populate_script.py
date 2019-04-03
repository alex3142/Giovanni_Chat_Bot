import shutil

ingredient_template = """###  http://www.semanticweb.org/ontologies/2019/0/project_giovanni#{Ingredient}
:{Ingredient} rdf:type owl:Class ;
      rdfs:subClassOf :{Parent} ;
      rdfs:label "{ingredient}" ."""

recipe_inst_template = """###  http://www.semanticweb.org/ontologies/2019/0/project_giovanni#{Recipe}
:{Recipe} rdf:type owl:NamedIndividual ,
                  :{Cuisine}Cuisine ,
                  :Recipe ;
         rdfs:label "{recipe}" ;
         :hasRelatedUrl "{link}" ;
         :hasIngredient {ingredients}"""

recipe_ingr_template = """:{Recipe}_Ingredient{idx}"""

ingr_inst_template = """###  http://www.semanticweb.org/ontologies/2019/0/project_giovanni#{Recipe}_Ingredient{idx}
:{Recipe}_Ingredient{idx} rdf:type owl:NamedIndividual ,
                              :{Ingredient} .
"""


def main():

    shutil.copyfile('resources/project_giovanni.0.2.ttl', 'resources/project_giovanni.0.3.ttl')
    with open('resources/project_giovanni.0.2.ttl', 'a') as out:
        fd = open('resources/ontology_data_for_demo.csv')
        # Discard header
        fd.readline()

        count = 0
        for line in fd:
            recipe, ingr_group, cuisine, link = line.strip().split(",")

            recipe_data = {
                "recipe": recipe,
                "Recipe": recipe.replace(" ", "_").capitalize(),
                "Cuisine": cuisine.capitalize(),
                "link": link
            }

            ingredients = []
            for idx, ingr_str in enumerate(ingr_group.split("\t")):
                parent, ingredient = ingr_str.split('#')

                ingredient_data = {
                    "ingredient": ingredient,
                    "Ingredient": ingredient.replace(" ", "_").capitalize(),
                    "idx": idx+1,
                    "Parent": parent.replace(" ", "_").capitalize()
                }
                ingredient_data.update(recipe_data)

                print(ingredient_template.format(**ingredient_data), file=out)
                print(file=out)
                print(ingr_inst_template.format(**ingredient_data), file=out)
                ingredients.append(recipe_ingr_template.format(**ingredient_data))

            recipe_data["ingredients"] = """ ,
               """.join(ingredients) + " .\n"

            print(recipe_inst_template.format(**recipe_data), file=out)

            count += 1
            # if count > 5:
            #     break


if __name__ == "__main__":
    main()
