/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.hadoop.metrics2.sink;

import org.apache.hadoop.metrics2.AbstractMetric;
import org.apache.hadoop.metrics2.MetricsRecord;

public class SqlServerSinkHadoop2 extends SqlServerSink {
  public SqlServerSinkHadoop2() {
    super(SqlSink.HADOOP2_NAMENODE_URL_KEY, SqlSink.HADOOP2_DFS_BLOCK_SIZE_KEY);
  }

  @Override
  public void putMetrics(MetricsRecord record) {
    long metricRecordID = getMetricRecordID(record.context(), record.name(),
            getLocalNodeName(), getLocalNodeIPAddress(), getClusterNodeName(), getCurrentServiceName(),
            getTagString(record.tags()), record.timestamp());
    if (metricRecordID < 0)
      return;

    for (AbstractMetric metric : record.metrics()) {
      insertMetricValue(metricRecordID, metric.name(), String.valueOf(metric.value()));
      if (metric.name().equals("BlockCapacity")) {
        insertMetricValue(metricRecordID, "BlockSize", Integer
                .toString(getBlockSize()));
      }
    }
  }
}
