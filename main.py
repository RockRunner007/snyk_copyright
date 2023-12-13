import json

import requests

#https://api.clearlydefined.io/definitions/maven/mavencentral/org.jacoco/org.jacoco.ant/0.8.9
copyright_url = 'https://api.clearlydefined.io/definitions/{repo_def}/{namespace}/{package}/{version}'

sbom_out = None
copyrights = {}

def get_copyright(sbom_out):

    def repo_def_lookup(repo_def):

        repo_defs = {
            'maven': 'maven/mavencentral'
        }

        return repo_defs[repo_def.split(':')[1]]

    with open(sbom_out, 'r')as f_open:
        sbom_json = json.loads(f_open.read())

    for component in sbom_json['components']:

        purl_segments = component['purl'].split('/')

        copyright_url_form = copyright_url.format(
            repo_def=repo_def_lookup(purl_segments[0]),
            namespace=purl_segments[1] if len(purl_segments) == 3 else '-', #not all pURLs have namespaces
            package=purl_segments[len(purl_segments) - 1].split('@')[0],
            version=purl_segments[len(purl_segments) - 1].split('@')[1]
        )

        print('COPYRIGHT URL ' + copyright_url_form)

        copyright_info = requests.get(copyright_url_form).json()

        copyrights[component['purl']] = {file['license']: file['attributions'] if 'attributions' in file else []
                                         for file in copyright_info['files']
                                         if 'license' in file}

        print(copyrights)


if __name__ == '__main__':
    get_copyright("/Users/jordanmiles/Documents/GitHub/corda-cli-plugin-host/sbom_out.json")

