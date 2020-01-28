# ESIM（Enhanced LSTM for Natural Language Inference）

## 模型结构

Overall inference models模型去除了树模型部分，只采用左半部分的序列模型，作者称它为**ESIM**。实验结果也表明了ESIM超越了之前的最好成绩。也可以通过结合树LSTM神经网络编码句法信息，作者把它与ESIM相结合得到混合模型称为**HIM**。

* 输入编码（input encoding）
* 局部推理模型（local inference modeling）
* 推理合成（inference composition）

### 输入编码（input encoding）

利用BiLSTM（或者Tree-LSTM）模块作为推理模型的一个基础模块，用它对输入单词（前提和假设）进行编码。这里BiLSTM可以通过学习表征单词和它的上下文信息（因为BiLSTM能够很好的表征局部推理信息和它在上下文中的影响）。

### 局部推理（local inference modeling）

建立前提与假设之间的局部推理模型。局部推理模型需要采用一些硬对齐或软对齐机制来关联前提和假设之间的单词序列；在神经网络模型中，实现对齐机制经常采用的是注意力机制。

第一部分：
* Local inference collected over sequences：针对BiLSTM产生的输出
* Local inference collected over parse trees：针对Tree-LSTM产生的输出（Tree-LSTM用树模型来帮助采集局部推断中关于语言短语和从句方面的信息）。

第二部分：
* Enhancement of local inference information：进一步增强收集到的局部推理信息。作者期望这样的操作可以帮助锐化元组中元素之间的局部推理信息，并捕获诸如矛盾等推理关系。**计算得到的差异和点积向量拼接在原始向量之后**；对序列模型和树模型都进行了这样的增强方式。得到m\_a和m\_b。

### 推理合成（inference composition）

利用整合层来组合增强的局部推理信息m\_a和m\_b。

第一部分：
* Composition Layer：使用BiLSTM（或者Tree-LSTM）来整合局部推断信息。

第二部分：
* Pooling Layer：将上述得到的结果向量经池化后转换成定长向量，并将其提供给最终的分类器以确定整个推理关系。作者认为直接求和操作可能对序列长度比较敏感，因此模型的鲁棒性会较差。所以作者建议采用以下策略：计算平均池化和最大池化，并将这些向量进行拼接，形成最终的固定长度向量v。**作者的实验也表明，这比直接求和有更好的效果**。

## 参考

[ESIM模型介绍](https://zhuanlan.zhihu.com/p/86978155)

