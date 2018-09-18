# -*- coding: utf-8 -*-
# Copyright 2018 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade
from odoo import tools


def populate_base_comment_template(cr):
    cr.execute(
        """
        INSERT INTO base_comment_template (name, text, position, old_id, _old_module_type)
        SELECT name, text, CASE
                    WHEN type = 'header' THEN 'before_lines'
                    WHEN type = 'footer' THEN 'after_lines'
                    ELSE type
                END AS position, id as old_id, 'sale' as _old_module_type 
        FROM sale_condition_text
        """
    )


def update_sale_order(cr):
    cr.execute(
        """
        UPDATE sale_order so
        SET comment_template1_id = bct.id
        FROM base_comment_template bct
        WHERE so.%s = bct.old_id AND bct.position = 'before_lines'
		AND bct._old_module_type = 'sale'
        """ % openupgrade.get_legacy_name('text_condition1')
    )
    cr.execute(
        """
        UPDATE sale_order so
        SET comment_template2_id = bct.id
        FROM base_comment_template bct
        WHERE so.%s = bct.old_id AND bct.position = 'after_lines'
		AND bct._old_module_type = 'sale'
        """ % openupgrade.get_legacy_name('text_condition2')
    )


@openupgrade.migrate(use_env=False)
def migrate(cr, version):
    populate_base_comment_template(cr)
    update_sale_order(cr)
    tools.drop_view_if_exists(cr, 'sale_condition_text')
