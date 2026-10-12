"""unittestとpytestの両方で実行できるテスト。"""
import copy
import unittest

from curry_python_simulator import (
    make_recipe, requirements, shortages, reserve, new_job, move,
    prepare, heat, plate, is_complete, run_simulation,
)


class CurryTests(unittest.TestCase):
    def setUp(self):
        self.recipe = make_recipe()
        self.needed = requirements(self.recipe, 2)
        self.stock = {
            name: amount + 10
            for name, amount in self.needed.items()
        }

    def prepared(self):
        job = new_job(self.recipe, 2)
        return prepare(move(job, "reserved", "材料確保"))

    def test_amounts_for_two(self):
        self.assertEqual(self.needed["肉_g"], 200)
        self.assertEqual(self.needed["水_ml"], 500)

    def test_minimum_servings(self):
        self.assertEqual(requirements(self.recipe, 1)["肉_g"], 100)

    def test_maximum_servings(self):
        self.assertEqual(requirements(self.recipe, 20)["肉_g"], 2000)

    def test_out_of_range(self):
        for value in (0, -1, 21):
            with self.subTest(value=value), self.assertRaises(ValueError):
                requirements(self.recipe, value)

    def test_wrong_serving_types(self):
        for value in (True, 2.0, "2", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                requirements(self.recipe, value)

    def test_exact_stock(self):
        self.assertEqual(shortages(self.needed, self.needed), {})

    def test_one_unit_short(self):
        self.stock["肉_g"] = 199
        self.assertEqual(
            shortages(self.stock, self.needed), {"肉_g": 1}
        )

    def test_missing_key(self):
        del self.stock["肉_g"]
        self.assertEqual(
            shortages(self.stock, self.needed), {"肉_g": 200}
        )

    def test_multiple_shortages(self):
        self.assertEqual(shortages({}, {"肉_g": 100, "水_ml": 250}),
                         {"肉_g": 100, "水_ml": 250})

    def test_reserve_does_not_mutate(self):
        before = self.stock.copy()
        remaining = reserve(self.stock, self.needed)
        self.assertEqual(self.stock, before)
        self.assertTrue(all(v == 10 for v in remaining.values()))

    def test_failed_reserve_is_all_or_nothing(self):
        self.stock["ルー_g"] = 0
        before = self.stock.copy()
        with self.assertRaises(ValueError):
            reserve(self.stock, self.needed)
        self.assertEqual(self.stock, before)

    def test_extra_stock_preserved(self):
        self.stock["茶葉_g"] = 80
        self.assertEqual(reserve(self.stock, self.needed)["茶葉_g"], 80)

    def test_negative_stock_rejected(self):
        self.stock["肉_g"] = -1
        with self.assertRaises(ValueError):
            run_simulation(self.recipe, 2, self.stock)

    def test_stock_type_rejected(self):
        for value in (1.5, True, "200"):
            with self.subTest(value=value), self.assertRaises(TypeError):
                shortages({"肉_g": value}, {"肉_g": 100})

    def test_recipe_instances_independent(self):
        second = make_recipe()
        self.recipe["per_person"]["肉_g"] = 1
        self.assertEqual(second["per_person"]["肉_g"], 100)

    def test_bad_recipe_kind(self):
        with self.assertRaises(ValueError):
            make_recipe("unknown")

    def test_invalid_recipe_amount(self):
        self.recipe["per_person"]["肉_g"] = 0
        with self.assertRaises(ValueError):
            requirements(self.recipe, 2)

    def test_invalid_heat_target(self):
        self.recipe["heat_steps"] = 0
        with self.assertRaises(ValueError):
            new_job(self.recipe, 2)

    def test_new_job_detaches_recipe(self):
        job = new_job(self.recipe, 2)
        self.recipe["per_person"]["肉_g"] = 500
        self.assertEqual(job["needed"]["肉_g"], 200)

    def test_prepare_requires_reservation(self):
        with self.assertRaises(RuntimeError):
            prepare(new_job(self.recipe, 2))

    def test_heat_requires_preparation(self):
        with self.assertRaises(RuntimeError):
            heat(new_job(self.recipe, 2))

    def test_heat_one_step(self):
        job = self.prepared()
        updated = heat(job)
        self.assertEqual(updated["heat_done"], 1)
        self.assertEqual(job["heat_done"], 0)
        self.assertEqual(job["history"][-1], "下ごしらえ完了")

    def test_snapshot_not_shared(self):
        job = self.prepared()
        updated = heat(job)
        updated["needed"]["肉_g"] = 1
        updated["history"].append("試験")
        self.assertEqual(job["needed"]["肉_g"], 200)
        self.assertNotIn("試験", job["history"])

    def test_cannot_plate_early(self):
        with self.assertRaises(RuntimeError):
            plate(self.prepared())

    def test_heating_boundary(self):
        job = self.prepared()
        for _ in range(5):
            job = heat(job)
        self.assertEqual(job["stage"], "heating")
        self.assertFalse(is_complete(job))
        job = heat(job)
        self.assertEqual(job["stage"], "cooked")
        self.assertFalse(is_complete(job))
        self.assertTrue(is_complete(plate(job)))

    def test_cannot_heat_twice_after_completion(self):
        job = self.prepared()
        for _ in range(6):
            job = heat(job)
        with self.assertRaises(RuntimeError):
            heat(job)

    def test_stove_failure_preserves_input(self):
        job = self.prepared()
        before = copy.deepcopy(job)
        with self.assertRaisesRegex(RuntimeError, "コンロ故障"):
            heat(job, False)
        self.assertEqual(job, before)

    def test_invalid_stove_flag(self):
        with self.assertRaises(TypeError):
            run_simulation(self.recipe, 2, self.stock, "yes")

    def test_fault_after_partial_heating(self):
        job = self.prepared()
        for _ in range(3):
            job = heat(job)
        before = copy.deepcopy(job)
        with self.assertRaises(RuntimeError):
            heat(job, False)
        self.assertEqual(job, before)
        self.assertEqual(job["heat_done"], 3)

    def test_cannot_plate_completed_job_again(self):
        result = run_simulation(self.recipe, 2, self.stock)
        with self.assertRaises(RuntimeError):
            plate(result["job"])

    def test_success(self):
        result = run_simulation(self.recipe, 2, self.stock)
        self.assertTrue(result["ok"])
        self.assertIsNone(result["error"])
        self.assertEqual(len(result["job"]["history"]), 10)
        self.assertTrue(
            all(v == 10 for v in result["remaining"].values())
        )

    def test_shortage_does_not_consume(self):
        self.stock["肉_g"] = 0
        result = run_simulation(self.recipe, 2, self.stock)
        self.assertFalse(result["ok"])
        self.assertEqual(result["remaining"], self.stock)
        self.assertEqual(result["job"]["stage"], "planned")

    def test_fault_keeps_reserved_stock_consumed(self):
        result = run_simulation(self.recipe, 2, self.stock, False)
        self.assertFalse(result["ok"])
        self.assertEqual(result["job"]["stage"], "prepared")
        self.assertEqual(result["remaining"]["肉_g"], 10)
        self.assertEqual(result["job"]["heat_done"], 0)

    def test_repeat_is_deterministic(self):
        before = copy.deepcopy((self.recipe, self.stock))
        a = run_simulation(self.recipe, 2, self.stock)
        b = run_simulation(self.recipe, 2, self.stock)
        self.assertEqual(a, b)
        self.assertEqual((self.recipe, self.stock), before)

    def test_second_batch_uses_returned_stock(self):
        a = run_simulation(self.recipe, 2, self.stock)
        b = run_simulation(self.recipe, 2, a["remaining"])
        self.assertFalse(b["ok"])

    def test_seafood(self):
        recipe = make_recipe("seafood")
        needed = requirements(recipe, 3)
        self.assertNotIn("肉_g", needed)
        self.assertEqual(needed["シーフード_g"], 300)
        result = run_simulation(recipe, 3, needed)
        self.assertTrue(result["ok"])
        self.assertEqual(result["job"]["heat_done"], 4)

    def test_custom_recipe(self):
        recipe = make_recipe()
        recipe["per_person"]["玉ねぎ_g"] = 90
        recipe["heat_steps"] = 1
        needed = requirements(recipe, 2)
        self.assertEqual(needed["玉ねぎ_g"], 180)
        self.assertTrue(run_simulation(recipe, 2, needed)["ok"])


if __name__ == "__main__":
    unittest.main()