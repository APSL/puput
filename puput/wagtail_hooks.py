import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler
from wagtail.core import hooks


@hooks.register('register_rich_text_features')
def register_blockquote_feature(features):
    """
    Registering the `blockquote` feature, which uses the `blockquote` Draft.js block type,
    and is stored as HTML with a `<blockquote>` tag.
    """
    feature_name = 'blockquote'
    type_ = 'blockquote'
    tag = 'blockquote'

    control = {
        'type': type_,
        'label': '❝',
        'description': 'Quote',
        'element': 'blockquote',
    }

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.BlockFeature(control)
    )

    features.register_converter_rule(
        'contentstate',
        feature_name,
        {
            'from_database_format': {tag: BlockElementHandler(type_)},
            'to_database_format': {'block_map': {type_: tag}},
        }
    )
    features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_codeline_feature(features):
    feature_name = 'Code Line'
    type_ = 'CODE'
    tag = 'code'

    control = {
        'type': type_,
        'label': '>_',
        'description': 'Code Line',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)
    features.default_features.append(feature_name)
