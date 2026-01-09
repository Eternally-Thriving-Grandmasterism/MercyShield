from pythonforandroid.recipe import RustCompiledComponentsRecipe

class MercyPQCRecipe(RustCompiledComponentsRecipe):
    name = 'mercy_pqc'
    version = '0.2.0'
    src_filename = '../../../../Cargo.toml'  # Path from recipe dir to root Cargo.toml (adjust count if needed: up 6 levels typical)

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['CARGO_BUILD_TARGET'] = arch.target
        return env

recipe = MercyPQCRecipe()
