from setuptools import setup

setup(name='research_pubsub', version='0.1.0', packages=['research_pubsub'],
      data_files=[('share/ament_index/resource_index/packages',['resource/research_pubsub']),
                  ('share/research_pubsub',['package.xml'])],
      install_requires=['setuptools'], zip_safe=True,
      maintainer='Research example', maintainer_email='example@example.org',
      description='研知发布订阅实验', license='MIT',
      entry_points={'console_scripts':['talker = research_pubsub.nodes:talker',
                                       'listener = research_pubsub.nodes:listener']})
