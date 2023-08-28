import unittest
import numpy as np
import numpy.testing as npt
import pandas as pd

import os

from tercen.client import context as ctx
import tercen.util.builder as bld
import tercen.util.helper_functions as hlp
from src.operator_funcs import calc_mean

from tercen.model.base import Table, Column, InMemoryRelation, Relation, SchemaBase, SimpleRelation
from tercen.model.base import CompositeRelation, JoinOperator, ColumnPair

class TestOperator(unittest.TestCase):
    def setUp(self):
        envs = os.environ
        isLocal = False
        if 'TERCEN_PASSWORD' in envs:
            passw = envs['TERCEN_PASSWORD']
        else:
            passw = None

        if 'TERCEN_URI' in envs:
            serviceUri = envs['TERCEN_URI']
        else:
            serviceUri = None
        if 'TERCEN_USERNAME' in envs:
            username = envs['TERCEN_USERNAME']
        else:
            isLocal = True
            username = 'test'
            passw = 'test'
            conf = {}
            with open("./unittests/env.conf") as f:
                for line in f:
                    if len(line.strip()) > 0:
                        (key, val) = line.split(sep="=")
                        conf[str(key)] = str(val).strip()

            serviceUri = ''.join([conf["SERVICE_URL"], ":", conf["SERVICE_PORT"]])



        self.wkfBuilder = bld.WorkflowBuilder(serviceUri=serviceUri)
        self.wkfBuilder.create_workflow( 'python_auto_project', 'python_workflow')
        self.wkfBuilder.add_table_step( './tests/hospitals.csv' )

        name = self.shortDescription()
        self.wkfBuilder.add_data_step(yAxis={"name":"Procedure.Hip Knee.Cost", "type":"double"}, 
                                columns=[{"name":"Rating.Imaging", "type":"string"}],
                                rows=[{"name":"Rating.Effectiveness", "type":"string"}])
        
        
        if username is None: # Running locally
            self.context = ctx.TercenContext(
                            stepId=self.wkfBuilder.workflow.steps[1].id,
                            workflowId=self.wkfBuilder.workflow.id)
        else: # Running from Github Actions
            self.context = ctx.TercenContext(
                            username=username,
                            password=passw,
                            serviceUri=serviceUri,
                            stepId=self.wkfBuilder.workflow.steps[1].id,
                            workflowId=self.wkfBuilder.workflow.id)

        self.addCleanup(self.clear_workflow)
        
    def clear_workflow(self):
        self.wkfBuilder.clean_up_workflow()

    def test_row_col(self) -> None:
        '''row_col'''
        df = calc_mean(self.context)
        


        df = self.context.add_namespace(df.copy()) 
        resDf = self.context.save_dev(df.copy())

        assert( not resDf is None )
        assert(resDf.shape == df.shape)
        for i in range(0, len(resDf.columns)):
            c0 = df.columns[i] 
            c1 = resDf.columns[i] 

            npt.assert_array_almost_equal(df.loc[:,c0], resDf.select(c1).to_numpy().flatten())



if __name__ == '__main__':
    unittest.main()