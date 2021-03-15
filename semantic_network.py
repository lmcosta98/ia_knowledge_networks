

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None,rel_type=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (rel_type == None or isinstance(d.relation,rel_type))]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))
    
    # Ex1
    def list_associations(self):
        '''assoc_list = []
        
        for d in self.declarations:
            if isinstance(d.relation, Association) and d.relation.name not in assoc_list: 
                assoc_list.append(d.relation.name)

        return assoc_list'''

        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association)]))
    
    # Ex2
    def list_objects(self):
        return list(set([d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]))
    
    # Ex3
    def list_users(self):
        return list(set([d.user for d in self.declarations]))
    
    # Ex4
    def list_types(self):
        '''return list(set([d.relation.entity2 for d in self.declarations 
                         if isinstance(d.relation, (Member,Subtype))]))'''
        return list(set([d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype)] + 
                        [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member,Subtype))]))
    
    # Ex5
    def list_local_associations(self, entity):
        # return list(set(d.relation.name for d in self.declarations if isinstance(d.relation, Association) and (d.relation.entity1 == entity or d.relation.entity2 == entity))))
        return list(set(d.relation.name for d in self.declarations 
                        if isinstance(d.relation, Association) and entity in [d.relation.entity1, d.relation.entity2]))
    
    # Ex6
    def list_relations_by_user(self, user):
        return list(set([d.relation.name for d in self.declarations if d.user == user]))
    
    # Ex7
    def associations_by_user(self, user):
        return len(list(set([d.relation.name for d in self.declarations 
                             if isinstance(d.relation, Association) and d.user == user])))
    
    # Ex8
    def list_local_associations_by_user(self, entity):
        return list(set([(d.relation.name, d.user) for d in self.declarations 
             if isinstance(d.relation, Association) and entity in [d.relation.entity1, d.relation.entity2]]))
        
    # Ex9
    def predecessor(self, A, B):
        pred_b = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) 
                  and d.relation.entity1 == B]
        
        '''if pred_b == []:
            return False
        
        if A in pred_b:
            return True
        
        for p in pred_b:
            if self.predecessor(A, p):
                return True
        return False''' #tudo substituido pelo return abaixo
        
        return A in pred_b or any([self.predecessor(A,p) for p in pred_b])
    
    # Ex10        
    def predecessor_path(self, A, B):
        pred_b = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) 
                and d.relation.entity1 == B]      

        if A in pred_b:
            return [A, B]
        for path in [self.predecessor_path(A,p) for p in pred_b]:
            if not path is None:
                return path + [B]
        return None
    
    # Ex11-a)
    def query(self, entity, assoc_name=None):
        queries_pred_b = [self.query(d.relation.entity2, assoc_name) for d in self.declarations 
                          if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        
        return [d for sublist in queries_pred_b for d in sublist] + self.query_local(e1=entity, rel=assoc_name,rel_type=Association)
    
    # Ex11-b)        
    def query2(self, entity, rel_name=None):
        return self.query(entity, rel_name) + self.query_local(e1=entity, rel=rel_name, rel_type=(Member, Subtype))
        
    # Ex12
    def query_cancel(self, entity, assoc_name=None):
        queries_pred_entity = [self.query_cancel(d.relation.entity2, assoc_name) for d in self.declarations 
                               if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        
        local = self.query_local(e1=entity, rel=assoc_name,rel_type=Association) 
        return [f for f in [d for sublist in queries_pred_entity for d in sublist] 
                if f.relation.name not in [l.relation.name for l in local] ]  + local
    
    # Ex13
    def query_down(self, type_, assoc_name=None):
        queries_desc_entity = [self.query_down(d.relation.entity1, assoc_name) for d in self.declarations if isinstance(d.relation, (Member,Subtype))
                               and d.relation.entity2 == type_]

        return [d for sublist in queries_desc_entity for d in sublist] + self.query_local(e1=type_, rel=assoc_name, rel_type=Association)
        
        
        

