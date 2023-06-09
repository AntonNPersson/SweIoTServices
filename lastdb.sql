PGDMP     ,    *                {           SweIoTdb    15.1    15.1 5    t           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            u           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            v           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            w           1262    73769    SweIoTdb    DATABASE     ~   CREATE DATABASE "SweIoTdb" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Sweden.1252';
    DROP DATABASE "SweIoTdb";
                postgres    false            a          0    73791    batch 
   TABLE DATA           O   COPY public.batch (id, producer_id, production_comments, order_id) FROM stdin;
    public          postgres    false    221   X5       b          0    73811    config 
   TABLE DATA           L   COPY public.config (key, system_settings, application_settings) FROM stdin;
    public          postgres    false    222   �5       f          0    73833 	   customers 
   TABLE DATA           S   COPY public.customers (id, name, adress, warranty_time, purchase_data) FROM stdin;
    public          postgres    false    226   �5       n          0    73867    devices 
   TABLE DATA           ~   COPY public.devices (id, adress, config_key, customer_id, batch_id, mac_adress, serial_number, hw_version, fw_id) FROM stdin;
    public          postgres    false    234   �5       c          0    73818 	   firmwares 
   TABLE DATA           :   COPY public.firmwares (version, firmware, id) FROM stdin;
    public          postgres    false    223   W6       ]          0    73780    orders 
   TABLE DATA           w   COPY public.orders (id, order_date, order_quantity, order_information, delivered_date, delivered_quantity) FROM stdin;
    public          postgres    false    217   �6       [          0    73771 	   producers 
   TABLE DATA           5   COPY public.producers (id, name, adress) FROM stdin;
    public          postgres    false    215   �6       d          0    73825    role 
   TABLE DATA           <   COPY public.role (id, name, read, write, scope) FROM stdin;
    public          postgres    false    224   �6       p          0    81962    rsakeys 
   TABLE DATA           T   COPY public.rsakeys (id, privatekey, publickey, device_id, customer_id) FROM stdin;
    public          postgres    false    236   .7       j          0    73844    users 
   TABLE DATA           P   COPY public.users (id, name, email, role_id, customer_id, password) FROM stdin;
    public          postgres    false    230   �?       �           0    0    batch_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.batch_id_seq', 1, true);
          public          postgres    false    218            �           0    0    batch_order_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.batch_order_id_seq', 1, false);
          public          postgres    false    220            �           0    0    batch_producer_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.batch_producer_id_seq', 1, false);
          public          postgres    false    219            �           0    0    customers_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.customers_id_seq', 1, true);
          public          postgres    false    225            �           0    0    devices_batch_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.devices_batch_id_seq', 1, false);
          public          postgres    false    233            �           0    0    devices_customer_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.devices_customer_id_seq', 1, false);
          public          postgres    false    232            �           0    0    devices_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.devices_id_seq', 3, true);
          public          postgres    false    231            �           0    0    firmwares_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.firmwares_id_seq', 1, true);
          public          postgres    false    237            �           0    0    keys_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.keys_id_seq', 5, true);
          public          postgres    false    235            �           0    0    orders_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.orders_id_seq', 5, true);
          public          postgres    false    216            �           0    0    producers_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.producers_id_seq', 2, true);
          public          postgres    false    214            �           0    0    users_customer_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.users_customer_id_seq', 1, false);
          public          postgres    false    229            �           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 4, true);
          public          postgres    false    227            �           0    0    users_role_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_role_id_seq', 1, false);
          public          postgres    false    228            �           2606    73800    batch batch_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.batch
    ADD CONSTRAINT batch_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.batch DROP CONSTRAINT batch_pkey;
       public            postgres    false            �           2606    73817    config config_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.config
    ADD CONSTRAINT config_pkey PRIMARY KEY (key);
 <   ALTER TABLE ONLY public.config DROP CONSTRAINT config_pkey;
       public            postgres    false            �           2606    73840    customers customers_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.customers DROP CONSTRAINT customers_pkey;
       public            postgres    false            �           2606    73876    devices devices_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_pkey;
       public            postgres    false            �           2606    90164    firmwares firmwares_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT firmwares_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT firmwares_pkey;
       public            postgres    false            �           2606    81969    rsakeys keys_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.rsakeys
    ADD CONSTRAINT keys_pkey PRIMARY KEY (id);
 ;   ALTER TABLE ONLY public.rsakeys DROP CONSTRAINT keys_pkey;
       public            postgres    false            �           2606    81971    rsakeys keys_privatekey_key 
   CONSTRAINT     \   ALTER TABLE ONLY public.rsakeys
    ADD CONSTRAINT keys_privatekey_key UNIQUE (privatekey);
 E   ALTER TABLE ONLY public.rsakeys DROP CONSTRAINT keys_privatekey_key;
       public            postgres    false            �           2606    81973    rsakeys keys_publickey_key 
   CONSTRAINT     Z   ALTER TABLE ONLY public.rsakeys
    ADD CONSTRAINT keys_publickey_key UNIQUE (publickey);
 D   ALTER TABLE ONLY public.rsakeys DROP CONSTRAINT keys_publickey_key;
       public            postgres    false            �           2606    73787    orders orders_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public            postgres    false            �           2606    73778    producers producers_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.producers
    ADD CONSTRAINT producers_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.producers DROP CONSTRAINT producers_pkey;
       public            postgres    false            �           2606    73902    role role_name_key 
   CONSTRAINT     M   ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_name_key UNIQUE (name);
 <   ALTER TABLE ONLY public.role DROP CONSTRAINT role_name_key;
       public            postgres    false            �           2606    73831    role role_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.role DROP CONSTRAINT role_pkey;
       public            postgres    false            �           2606    73900    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public            postgres    false            �           2606    73898    users users_name_key 
   CONSTRAINT     O   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);
 >   ALTER TABLE ONLY public.users DROP CONSTRAINT users_name_key;
       public            postgres    false            �           2606    73853    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false            �           2606    73892    devices fk_batch    FK CONSTRAINT     p   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_batch FOREIGN KEY (batch_id) REFERENCES public.batch(id);
 :   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_batch;
       public          postgres    false    3241            �           2606    73887    devices fk_config_key    FK CONSTRAINT     y   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_config_key FOREIGN KEY (config_key) REFERENCES public.config(key);
 ?   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_config_key;
       public          postgres    false    3243            �           2606    73859    users fk_customer    FK CONSTRAINT     x   ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES public.customers(id);
 ;   ALTER TABLE ONLY public.users DROP CONSTRAINT fk_customer;
       public          postgres    false    3251            �           2606    73882    devices fk_customer    FK CONSTRAINT     z   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES public.customers(id);
 =   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_customer;
       public          postgres    false    3251            �           2606    81979    rsakeys fk_customer    FK CONSTRAINT     z   ALTER TABLE ONLY public.rsakeys
    ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES public.customers(id);
 =   ALTER TABLE ONLY public.rsakeys DROP CONSTRAINT fk_customer;
       public          postgres    false    3251            �           2606    81974    rsakeys fk_device    FK CONSTRAINT     t   ALTER TABLE ONLY public.rsakeys
    ADD CONSTRAINT fk_device FOREIGN KEY (device_id) REFERENCES public.devices(id);
 ;   ALTER TABLE ONLY public.rsakeys DROP CONSTRAINT fk_device;
       public          postgres    false    3259            �           2606    90165    devices fk_fw    FK CONSTRAINT     x   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_fw FOREIGN KEY (fw_id) REFERENCES public.firmwares(id) NOT VALID;
 7   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_fw;
       public          postgres    false    3245            �           2606    73806    batch fk_order    FK CONSTRAINT     o   ALTER TABLE ONLY public.batch
    ADD CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES public.orders(id);
 8   ALTER TABLE ONLY public.batch DROP CONSTRAINT fk_order;
       public          postgres    false    3239            �           2606    73801    batch fk_producer    FK CONSTRAINT     x   ALTER TABLE ONLY public.batch
    ADD CONSTRAINT fk_producer FOREIGN KEY (producer_id) REFERENCES public.producers(id);
 ;   ALTER TABLE ONLY public.batch DROP CONSTRAINT fk_producer;
       public          postgres    false    3237            �           2606    73854    users fk_role    FK CONSTRAINT     k   ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES public.role(id);
 7   ALTER TABLE ONLY public.users DROP CONSTRAINT fk_role;
       public          postgres    false    3249            a   !   x�3�4�I-.QHJ,I�042�4����� R��      b   "   x�342642�V*I-.Q�R�е\1z\\\ .r�      f   1   x�3�.O��I�LIMK,�)I7�40�!C�м���̒��=... (Xg      n   K   x�3�t,K��LIT�M�,���K,K�Q06�442"NC 43�20�2J�24�25��LIrV� a-g�W� �/a      c   "   x��6��Z�j����%+]�i����� �30      ]   )   x�3�4202�50�54�4�I-.Q�/JI-B����� �B	%      [      x�3���u�����/������ 2��      d   1   x�3��,.I�UpL����,.)J,�/�,Bc.C���Tǐ+F��� m_      p   n  x���K��6D�ӇqH$@�w��>�3��~��gᘰ;��K�Ld&@珟?�l��?�"�bƧm�e��#��ȶ���߱�#gd���l�G��mԸjǸƌ곪o�g\+�W�Γk�*FW�q�>�����z��j㨭����3��9G��]ۙ{�xxG�����WNbn5k�íF#�{�x��V�W��cp��'}#��&#�1�~�oo�D�O��
}�ξ�W�:���_�<������q2���p�q�9�x�cr�+�qg��)x H��`�3O@��9M|r��s;�j���"��Q'����X��I�䒓���� ��]�2�ӗ�V|�ډ�xc|�����1D�<� 3�N���w��-x���$���ϕ���$�d�ho�
N���Nx0ٍ=�I��UG��<;�ʓ�w��tOPK�7<����*�d�lL�'&�x�dJ�9>��Y��V��<e�����e\	����>����^���k4�Pu�ʗ37v����҄��r\ns�w�d!9�D3n�GA0�p�+`�@�y�<~Q+��p�r.�cx@b�"�� �ϛ�xJ}�K/���pvr0ݐ�#�����	��[��c�^d/ED^��w����i��F8F>�LSOt}C���Ն�dRw�Xh^�h�a��)�N^�q�y����� y�N�g��'�0�UTՌ�,�b���	�P%ĸ�X��f�e��m)&`-�K�FC6�0��2��p��x�v��Ct0��� �x�V�k�$< S7<�#��4�>C�����qxw�HeZ�ɞp.a�|�G5�cK��#��C{'gp���{����:��Y���ҙ@/{a�b�;FkXj�2���z�n�M��~��@��`��ı�����残��� s����}϶���Ȁ�S�����GqV=M�9�E���/�������&BPG��K~�)���b��hg��)c�Ȇ: ��JC^XlhP��Wp�]���<�-]�'T3�;DN�p�ހ#$>��A��47�辌xy�X�����2�"j������&�F�c�����WKշ�k����F�z9 ���e&��v�;,&�_( FXsto"�Ǜ�]u��ݪ�pN��xS��@��Bx�� ��y��ꂟ�L�J}�=Z�Y���t���~d�گ6q�a���z��ţe�U��?`Zd�j��0)��k�Vg8��ԛ)&i=�e���y��>�D���:���G^�C�>T��Ku ��{��d�J �A�2�~��U��C������𒴡}*^����J��	�\�(�W`�'��T��0�7�4L�VH�@�RS!���f����ɑY�:j&��K�s����=�z�r�	,C�"�ϐ7���(l,� vV,�ԅ�9"�V�s����6I�{���R�E��5���*���>�6��fw�����q��j�.<��eO��\�v7�*���H����w���2�K�]7��^Tb��W���z)k���ϲ����g��]��Qs����၉ͼ�#��~B�W[~M��0J����B�Ӯ���"v�<��kN` ]�Z�g��@���]O$��tI��V���ˊ��a����O[�q.���*�-ybR�r�[xkg����#�.0����d:ޔӠ�}�cV�aD��	�Z��z[�Ց3c�Y�� �[5y,w8��:�aK=a������R�S�z�����=px�Zo#�,t�8�܍�q��{�o�T�<�:���{�7)�j,��3U���v�ݞk�X�K�f{W�#�/��l0�o��F��p��D,�\��'�>��`�j�S�\|�㬮��w_���E�eї�W��NQ�8#��m^u���No��M����nn�kW��v�W/ݝu�{[��㱟�[��jC�na3���S����x۵��N�X+RDoo ��2�
��t�O��*}�^�̺�����Z���u���}�#�=(X�o��ս��jg#_ߦ�v3����c@\(���ly?�Lo˅�+X��CfƝ�Mo8]��r����x�F�沎-_B)�N�^\x�a�s�U��ߩ���N�y����{O��R��c�n�`������{)󛝃l+�>8IEc����bqx���S���ӏ�c�������_�T�p      j   �   x�}��n�@ k�;\�{��v�h����CJ�w��`[>(�ׇ$}�M9��]~���&M��T����n[zq�n]k4o�O=�z,��|���X���b4-��#z4&Q��]6�c������D�j�d�N�0]�b�e֥�i�/2��R߯�=�������zjC��X�����	�x��
K8�#i�d�����6u]�Q     