import ast
import copy
import inspect
import os
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from recycling_audit import (bin_weights, bin_rows, net_weights, from_building,
                             material_total, building_report)


BINS = [
    {"location": "Cafeteria West", "material": "PAPER",   "weight": "1,250 g", "flagged": "no"},
    {"location": "Cafeteria East", "material": "plastic", "weight": "480 g",   "flagged": "yes"},
    {"location": "Library",        "material": "Paper",   "weight": "2,015 g", "flagged": "no"},
    {"location": "Gym Lobby",      "material": "GLASS",   "weight": "935 g",   "flagged": "yes"},
    {"location": "Library Annex",  "material": "paper",   "weight": "60 g",    "flagged": "no"},
]

EMPTY_REPORT = {'bins': 0, 'grams': 0, 'flagged': 0}


def fresh():
    return copy.deepcopy(BINS)


def one(location="Art Room", material="CARDBOARD", weight="1,005 g", flagged="no"):
    return {"location": location, "material": material, "weight": weight, "flagged": flagged}


def body_of(func):
    """Parse a function's source and return its statements, minus any docstring."""
    tree = ast.parse(textwrap.dedent(inspect.getsource(func)))
    body = tree.body[0].body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    return body


def nodes_in(func):
    return [node for stmt in body_of(func) for node in ast.walk(stmt)]


def calls_name(func, name):
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name
               for n in nodes_in(func))


LOOPS = (ast.For, ast.While, ast.AsyncFor)
COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


class NoMutationMixin:

    def assert_not_mutated(self, data):
        self.assertEqual(data, BINS)
        for b in data:
            self.assertIsInstance(b["weight"], str, "the original weights must still be strings")
            self.assertNotIn("grams", b, "the original dicts must not gain a \"grams\" key")

    def assert_map_lambda_single_return(self, func):
        body = body_of(func)
        nodes = nodes_in(func)
        self.assertEqual(len(body), 1, "body must be a single statement")
        self.assertIsInstance(body[0], ast.Return, "body must be a single return statement")
        self.assertTrue(calls_name(func, 'map'), "must use map()")
        self.assertTrue(any(isinstance(n, ast.Lambda) for n in nodes), "must use a lambda")
        self.assertFalse(any(isinstance(n, LOOPS) for n in nodes), "no loops")
        self.assertFalse(any(isinstance(n, COMPREHENSIONS) for n in nodes), "no comprehensions")

    def assert_map_and_filter_no_loops(self, func):
        nodes = nodes_in(func)
        self.assertTrue(calls_name(func, 'map'), "must use map()")
        self.assertTrue(calls_name(func, 'filter'), "must use filter()")
        self.assertFalse(any(isinstance(n, LOOPS) for n in nodes), "no loops")


class TestTierB(NoMutationMixin, unittest.TestCase):

    def test_bin_weights(self):
        self.assertEqual(bin_weights(fresh()), [1250, 480, 2015, 935, 60])

    def test_bin_rows(self):
        self.assertEqual(bin_rows(fresh()), [
            {'location': 'Cafeteria West', 'grams': 1250},
            {'location': 'Cafeteria East', 'grams': 480},
            {'location': 'Library', 'grams': 2015},
            {'location': 'Gym Lobby', 'grams': 935},
            {'location': 'Library Annex', 'grams': 60},
        ])

    def test_bin_weights_are_integers(self):
        for grams in bin_weights(fresh()):
            self.assertIsInstance(grams, int)

    def test_empty_input(self):
        self.assertEqual(bin_weights([]), [])
        self.assertEqual(bin_rows([]), [])

    def test_single_element(self):
        self.assertEqual(bin_weights([one()]), [1005])
        self.assertEqual(bin_rows([one()]), [{'location': 'Art Room', 'grams': 1005}])

    def test_returns_list_not_map_object(self):
        self.assertIsInstance(bin_weights(fresh()), list)
        self.assertIsInstance(bin_rows(fresh()), list)

    def test_repeat_calls_give_same_result(self):
        data = fresh()
        self.assertEqual(bin_weights(data), bin_weights(data))
        self.assertEqual(bin_rows(data), bin_rows(data))

    def test_does_not_mutate_input(self):
        data = fresh()
        bin_weights(data)
        bin_rows(data)
        self.assert_not_mutated(data)

    def test_bin_rows_exact_keys(self):
        for row in bin_rows(fresh()):
            self.assertEqual(set(row), {'location', 'grams'})

    def test_constraint_map_lambda_single_return(self):
        for func in (bin_weights, bin_rows):
            with self.subTest(function=func.__name__):
                self.assert_map_lambda_single_return(func)


class TestTierBPlus(NoMutationMixin, unittest.TestCase):

    def test_net_weights(self):
        self.assertEqual(net_weights(fresh()), [1250, 430, 2015, 885, 60])

    def test_unflagged_bins_keep_their_weight(self):
        unflagged = [net_weights(fresh())[i] for i in (0, 2, 4)]
        self.assertEqual(unflagged, [1250, 2015, 60],
                         "the unflagged bins came back as 0; check the order of operations "
                         "in your expression: which part is Python treating as the choice?")

    def test_flagged_bin_loses_50(self):
        self.assertEqual(net_weights([one(flagged="yes")]), [955])

    def test_net_weights_are_integers(self):
        for grams in net_weights(fresh()):
            self.assertIsInstance(grams, int)

    def test_empty_input(self):
        self.assertEqual(net_weights([]), [])

    def test_single_element(self):
        self.assertEqual(net_weights([one()]), [1005])

    def test_returns_list_not_map_object(self):
        self.assertIsInstance(net_weights(fresh()), list)

    def test_repeat_calls_give_same_result(self):
        data = fresh()
        self.assertEqual(net_weights(data), net_weights(data))

    def test_does_not_mutate_input(self):
        data = fresh()
        net_weights(data)
        self.assert_not_mutated(data)

    def test_constraint_map_lambda_single_return(self):
        self.assert_map_lambda_single_return(net_weights)


class TestTierAMinus(NoMutationMixin, unittest.TestCase):

    def test_library_finds_both_bins(self):
        self.assertEqual(from_building(fresh(), "Library"), [
            {'location': 'Library', 'grams': 2015},
            {'location': 'Library Annex', 'grams': 60},
        ], "a location only has to contain the word, not equal it")

    def test_cafeteria(self):
        self.assertEqual(from_building(fresh(), "Cafeteria"), [
            {'location': 'Cafeteria West', 'grams': 1250},
            {'location': 'Cafeteria East', 'grams': 480},
        ])

    def test_gym_lobby(self):
        self.assertEqual(from_building(fresh(), "Gym Lobby"), [{'location': 'Gym Lobby', 'grams': 935}])

    def test_no_such_building(self):
        self.assertEqual(from_building(fresh(), "Pool"), [])

    def test_empty_input(self):
        self.assertEqual(from_building([], "Library"), [])

    def test_single_element(self):
        self.assertEqual(from_building([one()], "Art"), [{'location': 'Art Room', 'grams': 1005}])

    def test_returns_list_not_filter_or_map_object(self):
        self.assertIsInstance(from_building(fresh(), "Library"), list)
        self.assertIsInstance(from_building(fresh(), "Pool"), list)

    def test_repeat_calls_give_same_result(self):
        data = fresh()
        self.assertEqual(from_building(data, "Library"), from_building(data, "Library"))

    def test_does_not_mutate_input(self):
        data = fresh()
        from_building(data, "Library")
        self.assert_not_mutated(data)

    def test_exact_keys(self):
        for row in from_building(fresh(), "Cafeteria"):
            self.assertEqual(set(row), {'location', 'grams'})

    def test_constraint_map_and_filter_no_loops(self):
        self.assert_map_and_filter_no_loops(from_building)


class TestTierA(NoMutationMixin, unittest.TestCase):

    def test_paper_matches_every_capitalization(self):
        self.assertEqual(material_total(fresh(), "paper"), 3325)

    def test_plastic(self):
        self.assertEqual(material_total(fresh(), "plastic"), 480)

    def test_glass(self):
        self.assertEqual(material_total(fresh(), "glass"), 935)

    def test_no_such_material(self):
        self.assertEqual(material_total(fresh(), "metal"), 0)

    def test_empty_input(self):
        self.assertEqual(material_total([], "paper"), 0)

    def test_single_element(self):
        self.assertEqual(material_total([one()], "cardboard"), 1005)

    def test_returns_int(self):
        for material in ("paper", "metal"):
            with self.subTest(material=material):
                self.assertIsInstance(material_total(fresh(), material), int)

    def test_repeat_calls_give_same_result(self):
        data = fresh()
        self.assertEqual(material_total(data, "paper"), material_total(data, "paper"))

    def test_does_not_mutate_input(self):
        data = fresh()
        material_total(data, "paper")
        self.assert_not_mutated(data)

    def test_constraint_map_and_filter_no_loops(self):
        self.assert_map_and_filter_no_loops(material_total)


class TestTierAPlus(NoMutationMixin, unittest.TestCase):

    def test_cafeteria(self):
        self.assertEqual(building_report(fresh(), "Cafeteria"), {'bins': 2, 'grams': 1730, 'flagged': 1})

    def test_library(self):
        self.assertEqual(building_report(fresh(), "Library"), {'bins': 2, 'grams': 2075, 'flagged': 0})

    def test_gym_lobby(self):
        self.assertEqual(building_report(fresh(), "Gym Lobby"), {'bins': 1, 'grams': 935, 'flagged': 1})

    def test_building_with_no_bins(self):
        self.assertEqual(building_report(fresh(), "Pool"), EMPTY_REPORT)

    def test_empty_input(self):
        self.assertEqual(building_report([], "Library"), EMPTY_REPORT)

    def test_single_element(self):
        self.assertEqual(building_report([one(flagged="yes")], "Art"), {'bins': 1, 'grams': 1005, 'flagged': 1})

    def test_repeat_calls_give_same_result(self):
        data = fresh()
        self.assertEqual(building_report(data, "Cafeteria"), building_report(data, "Cafeteria"))

    def test_does_not_mutate_input(self):
        data = fresh()
        building_report(data, "Cafeteria")
        self.assert_not_mutated(data)

    def test_exact_keys(self):
        self.assertEqual(set(building_report(fresh(), "Cafeteria")), {'bins', 'grams', 'flagged'})

    def test_constraint_map_and_filter_no_loops(self):
        self.assert_map_and_filter_no_loops(building_report)


if __name__ == "__main__":
    unittest.main()
