import click
from buildutils import BuildConfiguration
from buildutils.plugins import CoveragePlugin, FlakePlugin,\
    GenericCommandPlugin, GenericCleanPlugin, EnsureVenvActivePlugin, with_alias, group_plugins


@click.command()
@click.option('--plugins', '-p')
@click.option('--list-plugins', '-l', is_flag=True)
def main(plugins: str, list_plugins: bool):
    plugin_names = plugins.split(',') if plugins is not None else []

    build_config = (
        BuildConfiguration()
        .config('build.ini')
        .plugins(
            EnsureVenvActivePlugin(),
            with_alias('clean', GenericCleanPlugin('CLEAN', 'Remove previous build files.')),
            with_alias('install', GenericCommandPlugin('INSTALL', 'Install required dependencies from requirements.txt file.')),
            FlakePlugin(),
            CoveragePlugin(),
            group_plugins(
                'generate-docs',
                GenericCommandPlugin('PREPARE_DOCS', 'Prepare Sphinx for generating documentation from inline comments.'),
                GenericCommandPlugin('GENERATE_DOCS', 'Generate documentation from inline comments using Sphinx')
            )
        )
    )

    if list_plugins:
        return build_config.print_available_plugins()

    build_config.build(plugin_names)


if __name__ == '__main__':
    main()
