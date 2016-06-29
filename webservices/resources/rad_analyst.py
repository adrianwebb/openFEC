from flask_apispec import doc

from webservices import args
from webservices import docs
from webservices import utils
from webservices import schemas
from webservices.common import models
from webservices.common.views import ApiResource


@doc(
    tags=['filer_resources'],
    description=docs.RAD_ANALYST,
)
class RadAnalystView(ApiResource):

    model = models.RadAnalyst
    schema = schemas.RadAnalystSchema
    page_schema = schemas.RadAnalystPageSchema

    filter_fulltext_fields = [
        ('name', model.name_txt),
    ]

    filter_multi_fields = [
        ('analyst_id', model.analyst_id),
        ('telephone_ext', model.telephone_ext),
        ('committee_id', model.committee_id),
    ]

    @property
    def args(self):
        return utils.extend(
            args.paging,
            args.rad_analyst,
            args.make_sort_args(
                validator=args.IndexValidator(models.RadAnalyst),
            ),
        )

    @property
    def index_column(self):
        return self.model.idx
