# type:ignore

import heroku3


def get_env_vars(filepath):
    print(f'Reading environment variables from {filepath}')
    with open(filepath) as f:
        lines = f.readlines()
    
    vars = {}
    for line in lines:
        name_val = line.split('=')
        name=name_val[0].strip()
        val=name_val[1].strip()
        print(f'{name}={val}')
        vars[name] = val

    return vars


def load_env_vars(vars, exclude=[]):
    print(f'Loading environment variables to Heroku')
    heroku_conn  = heroku3.from_key(vars['HEROKU_API_KEY'])
    app = heroku_conn.apps()['poeserver']
    for name,val in vars.items():
        if name not in exclude:
            print(f'{name}={val}')
            app.config()[name] = val


if __name__ == '__main__':
    vars = get_env_vars('.env.prod')
    load_env_vars(vars, exclude=['HEROKU_API_KEY'])