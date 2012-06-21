# -*- coding: utf-8 -*-

import os
import unittest

import ansible.utils

class TestUtils(unittest.TestCase):

    #####################################
    ### varLookup function tests

    def test_varLookup_list(self):
        vars = {
            'data': {
                'who': ['joe', 'jack', 'jeff']
            }
        }

        res = ansible.utils._varLookup('data.who', vars)

        assert sorted(res) == sorted(vars['data']['who'])

    #####################################
    ### varReplace function tests

    def test_varReplace_simple(self):
        template = 'hello $who'
        vars = {
            'who': 'world',
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == 'hello world'

    def test_varReplace_multiple(self):
        template = '$what $who'
        vars = {
            'what': 'hello',
            'who': 'world',
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == 'hello world'

    def test_varReplace_caps(self):
        template = 'hello $whoVar'
        vars = {
            'whoVar': 'world',
        }

        res = ansible.utils.varReplace(template, vars)
        print res
        assert res == 'hello world'

    def test_varReplace_middle(self):
        template = 'hello $who!'
        vars = {
            'who': 'world',
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == 'hello world!'

    def test_varReplace_alternative(self):
        template = 'hello ${who}'
        vars = {
            'who': 'world',
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == 'hello world'

    def test_varReplace_almost_alternative(self):
        template = 'hello $who}'
        vars = {
            'who': 'world',
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == 'hello world}'

    def test_varReplace_almost_alternative2(self):
        template = 'hello ${who'
        vars = {
            'who': 'world',
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == template

    def test_varReplace_alternative_greed(self):
        template = 'hello ${who} }'
        vars = {
            'who': 'world',
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == 'hello world }'

    def test_varReplace_notcomplex(self):
        template = 'hello $mydata.who'
        vars = {
            'data': {
                'who': 'world',
            },
        }

        res = ansible.utils.varReplace(template, vars)

        print res
        assert res == template

    def test_varReplace_nested(self):
        template = 'hello ${data.who}'
        vars = {
            'data': {
                'who': 'world'
            },
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == 'hello world'

    def test_varReplace_nested_int(self):
        template = '$what ${data.who}'
        vars = {
            'data': {
                'who': 2
            },
            'what': 'hello',
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == 'hello 2'

    def test_varReplace_unicode(self):
        template = 'hello $who'
        vars = {
            'who': u'wórld',
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == u'hello wórld'

    def test_varReplace_list(self):
        template = 'hello ${data[1]}'
        vars = {
            'data': [ 'no-one', 'world' ]
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == 'hello world'

    def test_varReplace_invalid_list(self):
        template = 'hello ${data[1}'
        vars = {
            'data': [ 'no-one', 'world' ]
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == template

    def test_varReplace_list_oob(self):
        template = 'hello ${data[2]}'
        vars = {
            'data': [ 'no-one', 'world' ]
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == template

    def test_varReplace_list_nolist(self):
        template = 'hello ${data[1]}'
        vars = {
            'data': { 'no-one': 0, 'world': 1 }
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == template

    def test_varReplace_nested_list(self):
        template = 'hello ${data[1].msg[0]}'
        vars = {
            'data': [ 'no-one', {'msg': [ 'world'] } ]
        }

        res = ansible.utils.varReplace(template, vars)

        assert res == 'hello world'

    #####################################
    ### Template function tests

    def test_template_basic(self):
        template = 'hello {{ who }}'
        vars = {
            'who': 'world',
        }

        res = ansible.utils.template(template, vars, {}, no_engine=False)

        assert res == 'hello world'

    def test_template_whitespace(self):
        template = 'hello {{ who }}\n'
        vars = {
            'who': 'world',
        }

        res = ansible.utils.template(template, vars, {}, no_engine=False)

        assert res == 'hello world\n'

    def test_template_unicode(self):
        template = 'hello {{ who }}'
        vars = {
            'who': u'wórld',
        }

        res = ansible.utils.template(template, vars, {}, no_engine=False)

        assert res == u'hello wórld'

    #####################################
    ### key-value parsing

    def test_parse_kv_basic(self):
        assert (ansible.utils.parse_kv('a=simple b="with space" c="this=that"') ==
                {'a': 'simple', 'b': 'with space', 'c': 'this=that'})
