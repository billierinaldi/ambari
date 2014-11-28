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
package org.apache.ambari.server.events;

/**
 * The {@link ServiceComponentInstalledEvent} class is fired when a service
 * component is successfully installed.
 */
public class ServiceComponentInstalledEvent extends ServiceEvent {
  private final String m_componentName;
  private final String m_hostName;

  /**
   * Constructor.
   *
   * @param clusterId
   * @param stackName
   * @param stackVersion
   * @param serviceName
   * @param componentName
   * @param hostName
   */
  public ServiceComponentInstalledEvent(long clusterId, String stackName,
      String stackVersion, String serviceName, String componentName,
      String hostName) {
    super(AmbariEventType.SERVICE_COMPONENT_INSTALL_SUCCESS, clusterId,
        stackName,
        stackVersion, serviceName);

    m_componentName = componentName;
    m_hostName = hostName;
  }

  /**
   * {@inheritDoc}
   */
  @Override
  public String toString() {
    StringBuilder buffer = new StringBuilder("ServiceComponentInstalledEvent{ ");
    buffer.append("cluserId=").append(m_clusterId);
    buffer.append(", stackName=").append(m_stackName);
    buffer.append(", stackVersion=").append(m_stackVersion);
    buffer.append(", serviceName=").append(m_serviceName);
    buffer.append(", componentName=").append(m_componentName);
    buffer.append(", hostName=").append(m_hostName);
    buffer.append("}");
    return buffer.toString();
  }
}