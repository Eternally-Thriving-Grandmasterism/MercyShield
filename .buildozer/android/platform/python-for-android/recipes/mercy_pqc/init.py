from pythonforandroid.recipe import RustCompiledComponentsRecipe

class MercyPQCRecipe(RustCompiledComponentsRecipe):
    name = 'mercy_pqc'
    version = '0.1.0'
    src_filename = '../../../Cargo.toml'  # Relative to recipe dir — adjust root resonance

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['CARGO_BUILD_TARGET'] = arch.target
        return env

recipe = MercyPQCRecipe()
